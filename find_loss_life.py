from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import warnings
import pandas as pd
import numpy as np
import time

from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import os

warnings.filterwarnings("ignore", category=UserWarning)     # 忽略警告

train_dir='D:/app/github/DQN_play_sekiro/loss_life/train'
test_dir='D:/app/github/DQN_play_sekiro/loss_life/test'
validation_dir='D:/app/github/DQN_play_sekiro/loss_life/validation'
train_dogs_dir=train_dir+'/loss_life'
train_cats_dir=train_dir+'/normal'
test_dogs_dir=test_dir+'/loss_life'
test_cats_dir=test_dir+'/normal'
validation_dogs_dir=validation_dir+'/loss_life'
validation_cats_dir=validation_dir+'/normal'

from tensorflow.keras.preprocessing.image import ImageDataGenerator


def image_show():
    datagen = ImageDataGenerator(rotation_range=40,
                                 width_shift_range=0.2,
                                 height_shift_range=0.2,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True,
                                 fill_mode='nearest')

    # 显示几个随机增强后的训练图像
    fnames = [os.path.join(train_dogs_dir, fname) for fname in os.listdir(train_dogs_dir)]
    img_path = fnames[1]
    img = image.load_img(img_path, target_size=(300, 300))  # 读取图像并调整图像大小
    x = image.img_to_array(img)  # 将其转换为形状（150,150,3）的numpy数组
    x = x.reshape((1,) + x.shape)  # 将其形状改变为（1,150,150,3）

    i = 0
    for batch in datagen.flow(x, batch_size=32):  # 要有多少就有多少
        plt.figure(i)
        print(batch[0].shape)
        imgplot = plt.imshow(image.array_to_img(batch[0]))
        i += 1
        if i % 3 == 0:
            break
    plt.show()


def create_model():
    # 定义一个包含dropout的新卷积神经网络
    from tensorflow.keras import models
    from tensorflow.keras import layers

    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(300, 300, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model


def train_model(model):
    from tensorflow.keras import optimizers
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizers.RMSprop(lr=1e-4),
                  metrics=['acc'])

    # 使用数据增强，只对训练数据进行增强，测试数据不进行增强
    train_datagen = ImageDataGenerator(rescale=1. / 255,
                                       rotation_range=40,
                                       width_shift_range=0.2,
                                       height_shift_range=0.2,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True, )
    test_datagen = ImageDataGenerator(rescale=1. / 255)  # 将所有图像缩小255倍，在0-1之间

    train_generator = train_datagen.flow_from_directory(train_dir,  # 目标目录
                                                        target_size=(300, 300),  # 调整图像大小为150*150
                                                        batch_size=10,
                                                        class_mode='binary')  # 使用了binary_corssentropy损失，所以用二进制标签
    validation_generator = test_datagen.flow_from_directory(validation_dir,  # 目标目录
                                                            target_size=(300, 300),  # 调整图像大小为150*150
                                                            batch_size=10,
                                                            class_mode='binary')  # 使用了binary_corssentropy损失，所以用二进制标签

    history = model.fit(train_generator,
                        steps_per_epoch=150,  # 从生成器中抽取steps_per_epoch个批量后（即运行了steps_per_epoch次梯度下降），拟合进入到下一轮次
                        epochs=150,  # 迭代150次
                        validation_data=validation_generator,
                        validation_steps=50)  # 从验证生成器中抽取多少个批次用于评估

    model.save('loss_life/model/loss_life_model.h5')
    pd.DataFrame(history.history).to_csv('loss_life/training_log1.csv', index=False)


def train_result():
    from tensorflow.keras.models import load_model
    model = load_model('loss_life/model/loss_life_model.h5')

    Data = pd.read_csv('loss_life/training_log1.csv')

    acc = np.array(Data['acc'])
    val_acc = np.array(Data['val_acc'])
    loss = np.array(Data['loss'])
    val_loss = np.array(Data['val_loss'])
    epochs = range(1, len(acc) + 1)
    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.figure()
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # image_show()
    train_model(create_model())
    train_result()