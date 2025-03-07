# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 21:10:06 2021

@author: pang
"""
import base64

import numpy as np
from grabscreen import grab_screen
import cv2
import time
import directkeys
from getkeys import key_check
import random
from DQN_tensorflow_gpu import DQN
import os
import pandas as pd
from restart import restart
import random
import tensorflow.compat.v1 as tf
# import tensorflow as tf
import requests, json
from logger import Logger


log = Logger('train.log', level='debug', fmt='%(asctime)s: %(message)s')

def pause_game(paused):
    KEY_P = 'P'
    KEY_L = 'L'
    keys = key_check()
    if KEY_P in keys:
        if paused:
            paused = False
            print('start game')
            time.sleep(1)
        else:
            paused = True
            print('pause game')
            time.sleep(1)
    if paused:
        print('paused')
        while True:
            keys = key_check()
            # pauses game and can get annoying.
            if KEY_P in keys:
                if paused:
                    paused = False
                    print('start game')
                    time.sleep(1)
                    break
                else:
                    paused = True
                    time.sleep(1)
            if KEY_L in keys:
                copy_profile(BOSS)
    return paused

def self_blood_count(self_gray):
    self_blood = 0
    # for self_bd_num in self_gray[469]:
    for self_bd_num in self_gray[1188][0:125]:
        # self blood gray pixel 80~98
        # 血量灰度值80~98
        # print('self:', self_bd_num)
        if self_bd_num > 60 and self_bd_num < 98:
            self_blood = self_blood + 1
    # np.set_printoptions(threshold=len(self_gray))
    # print(np.array(self_gray))
    # print('self:', self_blood)
    return self_blood


def boss_blood_count(boss_gray):
    boss_blood = 0
    for boss_bd_num in boss_gray[10]:
    # boss blood gray pixel 65~75
    # 血量灰度值65~75
    #     print('boss:', boss_bd_num)
        if boss_bd_num > 50 and boss_bd_num < 75:
            boss_blood = boss_blood + 1
    # print('boss:', boss_blood)
    return boss_blood

def take_action(action):
    if action == 0:     # T
        directkeys.lock_vision()
        directkeys.slash_attack()
    elif action == 1:   # T
        directkeys.lock_vision()
        directkeys.long_attack()
    elif action == 2:   # SPACE
        directkeys.lock_vision()
        directkeys.jump()
    elif action == 3:   # Y
        directkeys.lock_vision()
        directkeys.defense()
    elif action == 4:   # LSHIFT+D
        directkeys.lock_vision()
        directkeys.right_dodge()
    elif action == 5:   # LSHIFT+A
        directkeys.lock_vision()
        directkeys.left_dodge()

def get_action_name(action):
    if action == 0:
        return 'slash_attach'
    elif action == 1:
        return 'long_attack'
    elif action == 2:
        return 'jump'
    elif action == 3:
        return 'defense'
    elif action == 4:
        return 'right_dodge'
    elif action == 5:
        return 'left_dodge'


def action_judge(boss_blood, next_boss_blood, self_blood, next_self_blood, action, stop, emergence_break):
    # get action reward
    # emergence_break is used to break down training
    # 用于防止出现意外紧急停止训练防止错误训练数据扰乱神经网络
    if (self_blood == 0 and boss_blood == 0) \
            or (next_self_blood == 0 and next_boss_blood == 0):
        reward = 0
        done = 0
        stop = 0
        emergence_break = 100
        return reward, done, stop, emergence_break
    elif (self_blood == 0 and next_self_blood == 0):
        reward = 0
        done = 0
        stop = 0
        emergence_break = emergence_break + 1
        return reward, done, stop, emergence_break
    elif next_boss_blood - boss_blood == 0 and boss_blood > 0:         # when boss no harm
        if next_self_blood == 0 or ((next_self_blood - self_blood) > 90):     # self dead
            reward = -10
            done = 1
            stop = 0
            emergence_break = 0
        elif self_blood - next_self_blood > 5:      # self harm
            reward = -5
            done = 0
            stop = 0
            emergence_break = 0
        else:
            if action == 3 or action == 4 or action == 5: # defense or left_dodge or right_dodge
                reward = 1
                done = 0
                stop = 0
                emergence_break = emergence_break + 1
            else: # attack
                reward = -1
                done = 0
                stop = 0
                emergence_break = emergence_break + 1
        return reward, done, stop, emergence_break
    elif next_boss_blood - boss_blood > 200:   # boss loss 1 life
        if next_self_blood == 0 or ((next_self_blood - self_blood) > 90):     # self dead
            reward = -10
            done = 1
            stop = 0
            emergence_break = 0
        elif self_blood - next_self_blood > 5:      # self harm
            reward = 5
            done = 0
            stop = 0
            emergence_break = 0
        else:
            reward = 20
            done = 0
            stop = 0
            emergence_break = 0
        return reward, done, stop, emergence_break
    elif boss_blood - next_boss_blood > 3 and next_boss_blood > 0:  # boss harm
        if next_self_blood == 0 or ((next_self_blood - self_blood) > 90):  # self dead
            reward = -5
            done = 1
            stop = 0
            emergence_break = 0
        elif self_blood - next_self_blood > 5:  # self harm
            reward = 1
            done = 0
            stop = 0
            emergence_break = 0
        else:
            reward = 10
            done = 0
            stop = 0
            emergence_break = 0
        return reward, done, stop, emergence_break
    elif boss_blood - next_boss_blood > 3 and next_boss_blood == 0:  # boss dead by attack
        if next_self_blood == 0 or ((next_self_blood - self_blood) > 90):  # self dead
            reward = -5
            done = 1
            stop = 0
            emergence_break = 0
        elif self_blood - next_self_blood > 5:  # self harm
            reward = 10
            done = 0
            stop = 0
            emergence_break= 0
        else:
            reward = 20
            done = 0
            stop = 0
            emergence_break = 0
        return reward, done, stop, emergence_break
    elif self_blood > 0 and next_boss_blood == 0:  # boss dead anywhere
        reward = 20
        done = 0
        stop = 0
        emergence_break = 100
        return reward, done, stop, emergence_break
    else:
        reward = 0
        done = 0
        stop = 0
        emergence_break = 0
    return reward, done, stop, emergence_break


def recheck_next_blood(blood, next_blood):
    if abs(blood - next_blood) <= 5:
        return blood
    else:
        return next_blood


def copy_profile(boss_id):
    import os
    import shutil

    source_path = os.path.abspath(r'D:\\gain\\pytorch\\{}\\76561197960267366'.format(boss_id))
    target_path = os.path.abspath(r'C:\\Users\\Administrator\\AppData\\Roaming\\Sekiro\\76561197960267366')

    if os.path.exists(source_path):
        # 如果目标路径存在原文件夹的话就先删除
        shutil.rmtree(target_path)

    shutil.copytree(source_path, target_path)
    print('copy dir {} finished!'.format(boss_id))


def loss_life_predict(filename=None, img=None):
    try:
        loss_life_url = 'http://52.81.184.99:5005/predict'
        # data = json.dumps({'filename': filename})
        # r = requests.post(loss_life_url, json=data)
        if filename is None:
            files = {
                'img_path': img
            }
        else:
            files = {
                'img_path': open(filename, 'rb').read()
            }
        r = requests.post(loss_life_url, files=files, timeout=1)
        return r.json()['prediction']
    except Exception as e:
        log.logger.error('loss_life_predict fail: {}'.format(e))


BOSS = "boss_5_guixingbu"
DQN_model_path = "model_gpu_{}".format(BOSS)
DQN_log_path = "logs_gpu_{}/".format(BOSS)
WIDTH = 96
HEIGHT = 88
window_size = (600,104,1900,1430)
# station window_size

blood_window = (155,172,720,1373)
# used to get boss and self blood

action_size = 6
# action[n_choose,j,k,m,r]
# j-attack, k-jump, m-defense, r-dodge, n_choose-do nothing

EPISODES = 3000
big_BATCH_SIZE = 16
UPDATE_STEP = 50
# times that evaluate the network
num_step = 0
# used to save log graph
target_step = 0
# used to update target Q network
paused = True
# used to stop training

if __name__ == '__main__':
    copy_profile(BOSS)

    config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
    config.gpu_options.per_process_gpu_memory_fraction = 0.5
    config.gpu_options.allow_growth = True
    tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))

    agent = DQN(WIDTH, HEIGHT, action_size, DQN_model_path, DQN_log_path)
    # DQN init
    paused = pause_game(paused)
    # paused at the begin
    # 用于防止出现意外紧急停止训练防止错误训练数据扰乱神经网络
    for episode in range(EPISODES):
        # emergence_break is used to break down training
        emergence_break = 0
        screen_gray = cv2.cvtColor(grab_screen(window_size),cv2.COLOR_BGR2GRAY)
        # collect station gray graph
        blood_window_gray = cv2.cvtColor(grab_screen(blood_window),cv2.COLOR_BGR2GRAY)
        # collect blood gray graph for count self and boss blood
        station = cv2.resize(screen_gray,(WIDTH,HEIGHT))
        # change graph to WIDTH * HEIGHT for station input
        boss_blood = boss_blood_count(blood_window_gray)
        self_blood = self_blood_count(blood_window_gray)
        # count init blood
        target_step = 0
        # used to update target Q network
        done = 0
        total_reward = 0
        stop = 0
        # 用于防止连续帧重复计算reward
        last_time = time.time()
        while True:
            station = np.array(station).reshape(-1,HEIGHT,WIDTH,1)[0]
            # reshape station for tf input placeholder
            # print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            target_step += 1
            # get the action by state
            action = agent.Choose_Action(station)
            take_action(action)
            # take station then the station change
            screen_color = grab_screen(window_size)
            screen_gray = cv2.cvtColor(screen_color,cv2.COLOR_BGR2GRAY)
            # collect station gray graph
            blood_window_gray = cv2.cvtColor(grab_screen(blood_window),cv2.COLOR_BGR2GRAY)
            # collect blood gray graph for count self and boss blood
            next_station = cv2.resize(screen_gray,(WIDTH,HEIGHT))
            next_station = np.array(next_station).reshape(-1,HEIGHT,WIDTH,1)[0]
            next_boss_blood = recheck_next_blood(boss_blood, boss_blood_count(blood_window_gray))
            next_self_blood = recheck_next_blood(self_blood, self_blood_count(blood_window_gray))
            cv2.imwrite('F:/app/github/DQN_play_sekiro/imgs/%s.jpg' % (get_action_name(action)), screen_gray)
            if loss_life_predict(filename='F:/app/github/DQN_play_sekiro/imgs/%s.jpg' % (get_action_name(action))) == 0:
                # loss life
                log.logger.debug('detect loss life, self_blood set 0')
                next_self_blood = 0
            reward, done, stop, emergence_break = action_judge(boss_blood, next_boss_blood,
                                                               self_blood, next_self_blood,
                                                               action, stop, emergence_break)
            log.logger.debug('self_blood=%s->%s boss_blood=%s->%s action=%s reward=%s'
                  %(self_blood, next_self_blood, boss_blood, next_boss_blood, get_action_name(action), reward))

            # get action reward
            if emergence_break >= 100:
                # emergence break , save model and paused
                # 遇到紧急情况，保存数据，并且暂停
                print("emergence_break")
                agent.save_model()
                paused = True
                emergence_break = 0
            agent.Store_Data(station, action, reward, next_station, done)
            if len(agent.replay_buffer) > big_BATCH_SIZE:
                num_step += 1
                # save loss graph
                # print('train')
                agent.Train_Network(big_BATCH_SIZE, num_step)
            if target_step % UPDATE_STEP == 0:
                agent.Update_Target_Network()
                # update target Q network
            station = next_station
            self_blood = next_self_blood
            boss_blood = next_boss_blood
            total_reward += reward
            if paused:
                agent.save_model()
            paused = pause_game(paused)
            if done == 1:
                take_action(0)
                break
        if episode % 10 == 0:
            agent.save_model()
            # save model
        print('episode: ', episode, 'Evaluation Average Reward:', total_reward/target_step)
        restart()
        
            
            
            
            
            
        
        
    
    