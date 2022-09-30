#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

This program creates a toolbar.
The toolbar has one action, which
terminates the application, if triggered.

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QApplication, QLabel,
                         QTextEdit, QGridLayout, QWidget, QLineEdit,QMessageBox)
from PyQt5.QtGui import QIcon
from Ui_erc20transfer import Ui_Form
from contract import ERC20
from contract import ERC20Transfer
import csv
from web3 import Web3, HTTPProvider


airdropContract = "0xa063926bB9ef3Ee9a87D5B9a1B82299108353840"

class Example(QMainWindow, Ui_Form):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.pushButton_config.clicked.connect(self.pushbutton_config)
        self.pushButton_csvOk.clicked.connect(self.pushbutton_csvOk)
        self.pushButton_approve.clicked.connect(self.pushbutton_approve)
        self.pushButton_send.clicked.connect(self.pushbutton_send)
        self.config = {}
        self.airdrop_address = []
        self.address_number = 0
        self.token_number = 0
        self.token_contract = ""
        self.config_flag = False
        self.address_flag = False
        self.approve_flag = False
        self.send_flag = False

    # 空投配置
    def pushbutton_config(self):
        self.config['rpc'] = self.lineEdit_url.text()
        self.config['chainId'] = int(self.lineEdit_chainId.text())
        self.config['address'] = self.lineEdit_address.text()
        self.config['private'] = self.lineEdit_private.text()
        self.config['gasPrice'] = int(self.lineEdit_gas.text())
        self.config['contract'] = self.lineEdit_contract.text()
        self.token_contract = self.config['contract']
        config_message = "配置设置成功"
        for k, v in self.config.items():
            if v == "":
                config_message = k + "不能为空"

        QMessageBox.information(self, '提示', config_message)


        self.ERC20 = ERC20.ERC20(self.config)

        self.config['contract'] = airdropContract
        self.ERC20Transfer = ERC20Transfer.ERC20Transfer(self.config)
        self.config_flag = True

    # 空投地址配置
    def pushbutton_csvOk(self):
        if not self.config_flag:
            QMessageBox.information(self, '提示', "需要先确认配置")
            return

        self.airdrop_address = []
        self.address_number = 0
        self.token_number = 0

        f = self.textEdit_address.toPlainText()
        f = f.splitlines()
        QMessageBox.information(self, '提示', "输入成功")
        for row in f:
            row1 = row.split(',')
            self.airdrop_address.append(row1)
            self.address_number += 1
            self.token_number += float(row1[1])
        statusBarMessage = "空投地址数：{}，代币总额：{}".format(self.address_number, self.token_number)
        self.statusBar().showMessage(statusBarMessage)
        self.address_flag = True

    # 空投代币授权
    def pushbutton_approve(self):
        if not self.config_flag:
            QMessageBox.information(self, '提示', "需要先确认配置")
            return
        if not self.address_flag:
            QMessageBox.information(self, '提示', "需要先上传地址")
            return
        self.statusBar().showMessage("授权中...")
        self.ERC20.approve(airdropContract, Web3.toWei(self.token_number, 'ether'))
        self.statusBar().showMessage("授权成功")
        self.approve_flag = True


    # 空投代币发送
    def pushbutton_send(self):
        if not self.config_flag:
            QMessageBox.information(self, '提示', "需要先确认配置")
            return
        if not self.address_flag:
            QMessageBox.information(self, '提示', "需要先上传地址")
            return
        if not self.approve_flag:
            QMessageBox.information(self, '提示', "需要先授权代币")
            return
        toaddresses = []
        amoutns = []
        for row in self.airdrop_address:
            toaddresses.append(row[0])
            amoutns.append(Web3.toWei(row[1], 'ether'))
            
        self.statusBar().showMessage("发送中...")
        self.ERC20Transfer.batcTransfeFrom2(self.token_contract, toaddresses, amoutns)
        self.statusBar().showMessage("发送成功")
        self.send_flag = True
        self.approve_flag = False


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())