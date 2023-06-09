from PIL import Image, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, FloatField, SubmitField
from flask_wtf.recaptcha import RecaptchaField

app = Flask(__name__, template_folder='./flaskapp')

app.config['SECRET_KEY'] = '6LfV2nkmAAAAACIRRTKOB85-s0wZOwYJOxRNGoI5'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfV2nkmAAAAAFGuW5iYfpXc48TxbfjMJwbM-ci-'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfV2nkmAAAAACIRRTKOB85-s0wZOwYJOxRNGoI5'

def img_return(file1, file2):

    im_width = file1.width
    image1 = np.array(file1)
    image2 = np.array(file2)

    # Создание места для графиков и изображений
    fig = plt.figure(figsize=(14, 7))

    # Первое изображение
    p1 = fig.add_subplot(2, 2, 1)
    p1.set_title('Исходное изображение')
    p1.imshow(image1)

    # Второе изображение
    p2 = fig.add_subplot(2, 2, 2)
    p2.set_title('Полученное изображение')
    p2.imshow(image2)

    # График распределения цветов первого изображения
    ax1 = fig.add_subplot(2, 2, 3)
    ax1.set(xlim=(0, im_width), ylim=(0, 255))
    ax1.plot(np.mean(image1[:, :, 0], axis=0), 'r', label='Красный')
    ax1.plot(np.mean(image1[:, :, 1], axis=0), 'g', label='Зелёный')
    ax1.plot(np.mean(image1[:, :, 2], axis=0), 'b', label='Синий')
    ax1.set_xlabel('Ширина')
    ax1.set_ylabel('Цвет')
    ax1.set_title('Цветовые каналы исх. изображения')
    ax1.legend()

    # График распределения цветов второго изображения
    ax2 = fig.add_subplot(2, 2, 4)
    ax2.set(xlim=(0, im_width), ylim=(0, 255))
    ax2.plot(np.mean(image2[:, :, 0], axis=0), 'r', label='Красный')
    ax2.plot(np.mean(image2[:, :, 1], axis=0), 'g', label='Зелёный')
    ax2.plot(np.mean(image2[:, :, 2], axis=0), 'b', label='Синий')
    ax2.set_xlabel('Ширина')
    ax2.set_ylabel('Цвет')
    ax2.set_title('Цветовые каналы получ. изображения')
    ax2.legend()

    #Вывод всего на экран
    plt.savefig('static/result.png')
    #plt.show()

def f_bright_filter(file, brightness):
    # Create a brightness enhancer
    enhancer = ImageEnhance.Brightness(file)
    return enhancer.enhance(brightness)

class MyForm(FlaskForm):
    image = FileField('Выберите изображение')
    brightness = FloatField('Выберите яркость (от 0.0 до 2.0)')
    recaptcha = RecaptchaField()
    submit = SubmitField('Применить')

@app.route('/', methods=['GET', 'POST'])
def captcha():
    form = MyForm()
    if form.validate_on_submit():
        return render_template('one.html', form=form)
    return render_template('base.html', form=form)

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['image']
        f.save('transfer.jpg')
        file = Image.open("transfer.jpg")

        brightness = float(request.form['brightness'])
        img_return(file, f_bright_filter(file, brightness))

        return render_template("index.html")

# #Функция реализации обработки
# @app.route('/process', methods=['POST'])# вызов функции методом post
# def process():
#     #проверка на метод
#     if request.method == 'POST':
#         intensity = float(request.form['intensity'])
#         image_file = request.files['image']
#         image = Image.open(image_file)
#
#         color_intensity = {}
#         if request.form.get('color_red'):
#             color_intensity['r'] = intensity
#         if request.form.get('color_green'):
#             color_intensity['g'] = intensity
#         if request.form.get('color_blue'):
#             color_intensity['b'] = intensity
#
#         modified_image = modify_intensity(image, 1.0, color_intensity)
#         original_color_distribution = plot_color_distribution(image)
#         modified_color_distribution = plot_color_distribution(modified_image)
#
#         original_image_base64 = image_to_base64(image)
#         modified_image_base64 = image_to_base64(modified_image)
#
#         return render_template('result.html', original_image=original_image_base64,
#                                modified_image=modified_image_base64,
#                                original_color_distribution=original_color_distribution,
#                                modified_color_distribution=modified_color_distribution)
#     else:
#         return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
