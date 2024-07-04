import os

from django.shortcuts import render
from django.http import HttpResponse
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from moviepy.config import change_settings
from urllib.parse import quote

change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

def index(request):
    return render(request, 'index.html')

def generate_video(request, text=None):
    if request.method == 'POST':
        text = request.POST.get('text')
    elif text is None:
        return HttpResponse("Некорректный запрос", status=400)

    video_width, video_height = 100, 100
    duration = 3  # продолжительность видео в секундах
    fps = 24  # кадров в секунду

    # Создание текстового клипа с фиксированным размером шрифта, ширина не установлена
    txt_clip = TextClip(text, fontsize=100, color='white', size=(None, video_height))

    # Измеряем ширину текста
    text_width = txt_clip.w # возвращает ширину текста в пикселях

    # Выбираем множитель для ширины текста
    multiplier = 1.5

    # Создаем новый текстовый клип с шириной в 2 раза больше ширины текста
    txt_clip = TextClip(text, fontsize=100, color='white', size=(text_width * multiplier, video_height))
    txt_clip = txt_clip.set_duration(duration)

    # Определение анимации для текста
    def scroll_text(t):
        start_pos = video_width
        end_pos = -text_width * multiplier   # Учитываем ширину нового текстового клипа
        x_pos = start_pos + (end_pos - start_pos) * t / duration
        y_pos = (video_height - txt_clip.size[1]) / 2  # Центрирование текста по вертикали
        return (x_pos, y_pos)

    txt_clip = txt_clip.set_position(scroll_text)

    # создаем основное видео с черным фоном
    background = ColorClip(size=(video_width, video_height), color=(0, 0, 0), duration=duration)
    video = CompositeVideoClip([background, txt_clip])
    video = video.set_duration(duration)

    # сохраняем видео
    output_path = "output.mp4" # сохраняем видео
    video.write_videofile(output_path, codec='libx264', fps=fps)

    # чтение временного файла и отправка в ответе
    with open(output_path, "rb") as video_file:
        encoded_filename = quote(f"{text}.mp4")
        response = HttpResponse(video_file.read(), content_type="video/mp4")
        response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'

    os.remove(output_path) # удаляем временный файл

    return response