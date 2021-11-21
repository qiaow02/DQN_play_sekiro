# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 21:10:06 2021

@author: pang
"""

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

def pause_game(paused):
    KEY_P = 'P'
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
    return paused

def self_blood_count(self_gray):
    self_blood = 0
    # for self_bd_num in self_gray[469]:
    for self_bd_num in self_gray[1188]:
        # self blood gray pixel 80~98
        # 血量灰度值80~98
        # print('self:', self_bd_num)
        if self_bd_num > 70 and self_bd_num < 98:
            self_blood = self_blood + 1
    # np.set_printoptions(threshold=len(self_gray))
    # print(np.array(self_gray))
    # print('self:', self_blood)
    return self_blood

def boss_blood_count(boss_gray):
    boss_blood = 0
    for boss_bd_num in boss_gray[3]:
    # boss blood gray pixel 65~75
    # 血量灰度值65~75
    #     print('boss:', boss_bd_num)
        if boss_bd_num > 50 and boss_bd_num < 75:
            boss_blood = boss_blood + 1
    # print('boss:', boss_blood)
    return boss_blood

def take_action(action):
    if action == 0:     # n_choose
        directkeys.lock_vision()
        pass
    elif action == 1:   # T
        directkeys.lock_vision()
        directkeys.attack()
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
        return 'lock_vision'
    elif action == 1:
        return 'attack'
    elif action == 2:
        return 'jump'
    elif action == 3:
        return 'defense'
    elif action == 4:
        return 'right_dodge'
    elif action == 5:
        return 'left_dodge'


def action_judge(boss_blood, next_boss_blood, self_blood, next_self_blood, stop, emergence_break):
    # get action reward
    # emergence_break is used to break down training
    # 用于防止出现意外紧急停止训练防止错误训练数据扰乱神经网络
    if (self_blood == 0 and boss_blood == 0) \
            or (next_self_blood == 0 and next_boss_blood == 0)\
            or (self_blood == 0 and next_self_blood == 0):
        reward = 0
        done = 0
        stop = 0
        emergence_break = 100
        return reward, done, stop, emergence_break
    elif next_self_blood - self_blood > 40:     # self dead
        reward = -10
        done = 1
        stop = 0
        emergence_break = emergence_break + 1
        return reward, done, stop, emergence_break
    elif next_boss_blood - boss_blood == 0:     # boss no harm
        reward = -1
        done = 0
        stop = 0
        emergence_break = emergence_break + 1
        return reward, done, stop, emergence_break
    elif next_boss_blood - boss_blood > 15:   #boss loss 1 life
        reward = 20
        done = 0
        stop = 0
        emergence_break = emergence_break + 1
        return reward, done, stop, emergence_break
        # if emergence_break < 2:
        #     reward = 20
        #     done = 0
        #     stop = 0
        #     emergence_break = emergence_break + 1
        #     return reward, done, stop, emergence_break
        # else:
        #     reward = 20
        #     done = 0
        #     stop = 0
        #     emergence_break = 100
        #     return reward, done, stop, emergence_break
    else:
        self_blood_reward = 0
        boss_blood_reward = 0
        # print(next_self_blood - self_blood)
        # print(next_boss_blood - boss_blood)
        if next_self_blood - self_blood < -7:
            if stop == 0:
                self_blood_reward = -6
                stop = 1
                # 防止连续取帧时一直计算掉血
        else:
            stop = 0
        if next_boss_blood - boss_blood <= -3:
            boss_blood_reward = 4
        # print("self_blood_reward:    ",self_blood_reward)
        # print("boss_blood_reward:    ",boss_blood_reward)
        reward = self_blood_reward + boss_blood_reward
        done = 0
        emergence_break = 0
        return reward, done, stop, emergence_break


BOSS = "boss_2"
DQN_model_path = "model_gpu_{}".format(BOSS)
DQN_log_path = "logs_gpu_{}/".format(BOSS)
WIDTH = 96
HEIGHT = 88
window_size = (600,104,1900,1430)
# station window_size

blood_window = (155,172,520,1373)
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
    agent = DQN(WIDTH, HEIGHT, action_size, DQN_model_path, DQN_log_path)
    # DQN init
    paused = pause_game(paused)
    # paused at the begin
    emergence_break = 0     
    # emergence_break is used to break down training
    # 用于防止出现意外紧急停止训练防止错误训练数据扰乱神经网络
    for episode in range(EPISODES):
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
            screen_gray = cv2.cvtColor(grab_screen(window_size),cv2.COLOR_BGR2GRAY)
            # collect station gray graph
            blood_window_gray = cv2.cvtColor(grab_screen(blood_window),cv2.COLOR_BGR2GRAY)
            # collect blood gray graph for count self and boss blood
            next_station = cv2.resize(screen_gray,(WIDTH,HEIGHT))
            next_station = np.array(next_station).reshape(-1,HEIGHT,WIDTH,1)[0]
            next_boss_blood = boss_blood_count(blood_window_gray)
            next_self_blood = self_blood_count(blood_window_gray)
            reward, done, stop, emergence_break = action_judge(boss_blood, next_boss_blood,
                                                               self_blood, next_self_blood,
                                                               stop, emergence_break)
            print('self_blood=%s->%s boss_blood=%s->%s action=%s reward=%s'
                  %(self_blood, next_self_blood, boss_blood, next_boss_blood, get_action_name(action), reward))
            # cv2.imwrite('D:\\app\\github\\DQN_play_sekiro\\imgs\\self_blood=%s next_self_blood=%s boss_blood=%s next_boss_blood=%s action=%s reward=%s.jpg'
            #       %(self_blood, next_self_blood, boss_blood, next_boss_blood, get_action_name(action), reward), blood_window_gray)
            # get action reward
            if emergence_break == 100:
                # emergence break , save model and paused
                # 遇到紧急情况，保存数据，并且暂停
                print("emergence_break")
                agent.save_model()
                paused = True
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
                break
        if episode % 10 == 0:
            agent.save_model()
            # save model
        print('episode: ', episode, 'Evaluation Average Reward:', total_reward/target_step)
        restart()
        
            
            
            
            
            
        
        
    
    