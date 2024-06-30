import os

from django.shortcuts import render
from django.http import HttpResponse
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from moviepy.config import change_settings
from urllib.parse import quote

# указываем путь к исполняемому файлу convert.exe
change_settings({"IMAGEMAGICK_BINARY": "E:\\Programs\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

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

    # Создание бегущей строки
    txt_clip = TextClip(text, fontsize=70, color='white', size=(video_width * 5, None))
    txt_clip = txt_clip.set_duration(duration)

    # определение анимации для текста
    def scroll_text(t):
        x_pos = max(video_width - txt_clip.size[0], int(video_width - (video_width + txt_clip.size[0]) * t / duration))
        y_pos = (video_height - txt_clip.size[1]) / 2  # центрирование текста по вертикали
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