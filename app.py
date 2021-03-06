# -*- coding: utf-8 -*-
__version__ = '1.0.0'

import pickle, requests

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.actionbar import ActionBar, ActionButton, ActionView, ActionPrevious, ActionOverflow
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup 
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.core.window import Window
from kivy.uix.image import Image

import time
from master import Manager, APIHandler, TCPConnector, dobjs

class BlueFangApp(App):
    crnt_code = None
    
    def __init__(self):
        super().__init__()
        self.tcpobj = TCPConnector()
        self.manobj = Manager(self.tcpobj)
        self.loader()
        
    def loader(self):
        self.manobj.on_start()
    
    def main_screen(self):
        layout1 = BoxLayout(orientation='vertical')
        ab = ActionBar()
        layout11 = BoxLayout(orientation='horizontal')
        layout111 = BoxLayout(orientation='vertical', size_hint=(0.3,1))
        layout111.add_widget(Image(source ='back.png')) 
        
        tp = TabbedPanel(tab_pos = 'top_right', do_default_tab=False, size_hint = (0.7,1))
        ti1 = TabbedPanelItem(text='Down. list')
        ti2 = TabbedPanelItem(text='Info. list')
        tp.add_widget(ti1)
        tp.add_widget(ti2)
        self.down_list(ti1)
        self.info_list(ti2)
        
        abv =  ActionView()
        abv.add_widget(ActionPrevious(title='peer1', with_previous=False))
        abv.add_widget(ActionOverflow())
        abv.add_widget(ActionButton(text = 'New', on_press = self.new))
        abv.add_widget(ActionButton(text = 'Join', on_press = self.join))
        #abb = ActionButton()
        #abv.add_widget(abb)
        ab.add_widget(abv)
        
        layout11.add_widget(layout111)
        layout11.add_widget(tp)
        layout1.add_widget(layout11)
        layout1.add_widget(ab)
        
        return layout1
    
    def single_dwnload(self):
        def back(btn):
            self.sm.current = 'main'
        layout1 = BoxLayout(orientation='vertical')
        ab = ActionBar()
        layout11 = BoxLayout(orientation='horizontal')
        layout111 = BoxLayout(orientation='vertical', size_hint=(0.3,1))
        layout111.add_widget(Image(source ='back.png')) 
        
        tp = TabbedPanel(tab_pos = 'top_right', do_default_tab=False, size_hint = (0.7,1))
        ti1 = TabbedPanelItem(text='Details')
        tp.add_widget(ti1)
        self.ilist = ti1
        
        abv =  ActionView()
        abv.add_widget(ActionPrevious(title='peer1', with_previous=False))
        abv.add_widget(ActionOverflow())
        abv.add_widget(ActionButton(text = 'Back', on_press = back))
        #abb = ActionButton()
        #abv.add_widget(abb)
        ab.add_widget(abv)
        
        layout11.add_widget(layout111)
        layout11.add_widget(tp)
        layout1.add_widget(layout11)
        layout1.add_widget(ab)
        
        return layout1
    
    def single_info(self):
        def back(btn):
            self.sm.current = 'main'
        layout1 = BoxLayout(orientation='vertical')
        ab = ActionBar()
        layout11 = BoxLayout(orientation='horizontal')
        layout111 = BoxLayout(orientation='vertical', size_hint=(0.3,1))
        layout111.add_widget(Image(source ='back.png')) 
        
        tp = TabbedPanel(tab_pos = 'top_right', do_default_tab=False, size_hint = (0.7,1))
        ti1 = TabbedPanelItem(text='Dist. List')
        tp.add_widget(ti1)
        self.plist = ti1
        
        abv =  ActionView()
        abv.add_widget(ActionPrevious(title='peer1', with_previous=False))
        abv.add_widget(ActionOverflow())
        abv.add_widget(ActionButton(text = '4Back', on_press = back))
        #abb = ActionButton()
        #abv.add_widget(abb)
        ab.add_widget(abv)
        
        layout11.add_widget(layout111)
        layout11.add_widget(tp)
        layout1.add_widget(layout11)
        layout1.add_widget(ab)
        #layout1 = Label(text='hi')
        
        return layout1
        
    def build(self):
        
        self.title='Peer1'
        sm = ScreenManager()
        self.sm = sm
        main = Screen(name='main')
        single_info = Screen(name='single_info')
        single_dwnload = Screen(name='single_dwnload')
        main.add_widget(self.main_screen())
        single_info.add_widget(self.single_info())
        single_dwnload.add_widget(self.single_dwnload())  
        sm.add_widget(main)
        sm.add_widget(single_info)
        sm.add_widget(single_dwnload)
        
        return sm
    
    def down_list(self, widget):
        def dwn_sel(btn):
            self.crnt_code = btn.text
            self.dwnload_tab(self.ilist)
            self.sm.current = 'single_dwnload'
        layout112 = StackLayout(size_hint_y = None)
        layout112.bind(minimum_height=layout112.setter('height'))
        lay = ScrollView()
        lay.add_widget(layout112) 
        widget.add_widget(lay)
        print('')
        for code in dobjs:
            if code:
                layout112.add_widget(Button(text=code, size_hint_y=None, size=(0,50), on_press=dwn_sel))
        layout112.add_widget(Button(text=str(time.time()), size_hint_y=None, size=(0,50), on_press=dwn_sel))
                
    def info_list(self, widget):
        def dwn_sel(btn):
            self.crnt_code = btn.text
            self.peer_list(self.plist)
            self.sm.current = 'single_info'
        layout112 = StackLayout(size_hint_y = None)
        layout112.bind(minimum_height=layout112.setter('height'))
        lay = ScrollView()
        lay.add_widget(layout112) 
        widget.add_widget(lay)
        for code in self.manobj.apiobjs:
            if code:
                layout112.add_widget(Button(text=code, size_hint_y=None, size=(0,50), on_press=dwn_sel))
            
    def peer_list(self, widget):
        l1 = None
        peer = None
        ti1 = None
        def refresh_status(btn):
            nonlocal l1
            l1.text = f'{self.tcpobj.speak("localhost",self.crnt_code)}'
            
        def share_load(btn):
            nonlocal ti1, peer
            if int(ti1.text) > 0:
                self.tcpobj.speak(peer[0],self.crnt_code,int(ti1.text))
            
        def peer_item(btn):
            nonlocal l1, ti1, peer
            
            layout1 = BoxLayout(orientation = 'vertical')
            layout11 = BoxLayout(orientation = 'horizontal', size_hint=(1,.2))
            layout12 = BoxLayout(orientation = 'horizontal', size_hint=(1,.2))
            layout13 = BoxLayout(orientation = 'horizontal')
            layout12.add_widget(Label(text='Share (Bytes)',size_hint=(.3, .6)))
            ti1 = TextInput(size_hint=(.33, .6))
            layout12.add_widget(ti1)
            layout12.add_widget(Label(text='', size_hint=(.07, .6)))
            layout12.add_widget(Button(text='Confirm', size_hint=(.23, .6), on_press = share_load))
            layout12.add_widget(Label(text='', size_hint=(.07, .6)))
            l1 = Label(text=f'Download Status : Unknown', size_hint=(.7, .6))
            layout11.add_widget(l1)
            layout11.add_widget(Button(text='Refresh', size_hint=(.23, .6), on_press = refresh_status))
            layout11.add_widget(Label(text='', size_hint=(.07, .6)))
            layout1.add_widget(btn)
            layout1.add_widget(layout11)
            layout1.add_widget(layout12)
            layout1.add_widget(layout13)
            return layout1
        layout112 = StackLayout()
        widget.add_widget(layout112)
        
        self.manobj.fetch(self.crnt_code)
        ac = Accordion(orientation='vertical')
        layout112.add_widget(ac)
        print(self.manobj.peerdict)
        for ind, peer in enumerate(self.manobj.peerdict[self.crnt_code]):
            item = AccordionItem(title=f'Peer {ind+1}')
            item.add_widget(peer_item(Button(text=f'Range : {peer[1][0]} - {peer[1][1]}', size_hint_y=None)))            
            ac.add_widget(item)
    
    def dwnload_tab(self, widget):
        def refresh(btn):
            partdict = list(dobjs[self.crnt_code].partdict)
            l5.text = f'{partdict[1]-partdict[0]}'
            l7.text = f'{partdict[2]-partdict[1]}'
        layout = BoxLayout(orientation='vertical')
        layout1 = BoxLayout(orientation='horizontal',size_hint=(1,.15))
        l1 = Label(text='Url', size_hint=(.2,1))
        ti0 = TextInput(text=f'{dobjs[self.crnt_code].url}', size_hint=(.8,1))
        layout1.add_widget(l1)
        layout1.add_widget(ti0)
        partdict = list(dobjs[self.crnt_code].partdict)
        print(partdict)
        layout2 = BoxLayout(orientation='horizontal',size_hint=(1,.1))
        l2 = Label(text='Total Size :', size_hint=(.2,1))
        l3 = Label(text=f'{partdict[2]-partdict[0]}', size_hint=(.2,1))
        l4 = Label(text='Downloaded :', size_hint=(.2,1))
        l5 = Label(text=f'{partdict[1]-partdict[0]}', size_hint=(.2,1))
        l6 = Label(text='Balance :', size_hint=(.2,1))
        l7 = Label(text=f'{partdict[2]-partdict[1]}', size_hint=(.2,1))
        layout2.add_widget(l2)
        layout2.add_widget(l3)
        layout2.add_widget(l4)
        layout2.add_widget(l5)
        layout2.add_widget(l6)
        layout2.add_widget(l7)
        layout3 = StackLayout(orientation='rl-tb',size_hint=(1,.1))
        b1 = Button(text='Start', on_press=self.start, size_hint=(.5,1))
        b2 = Button(text='Refresh', on_press=refresh, size_hint=(.5,1))
        layout3.add_widget(b2)
        layout3.add_widget(b1)
        ti1 = TextInput(size_hint=(1,.9))
        layout.add_widget(layout1)
        layout.add_widget(layout2)
        layout.add_widget(layout3)
        layout.add_widget(ti1)
        widget.add_widget(layout)

    def start(self, btn):
        global pobjs
        if btn.text == 'Start':
            btn.text = 'Stop'
            Manager.dwnload_strt(self.crnt_code)
        else:
            btn.text = 'Start'
            Manager.dwnload_kill(self.crnt_code)
        
    def new(self, btn):
        def path_sel(btn):
            l2.text = fc.path
            fc_pop.dismiss()
        
        def dwnload(btn):
            url = ti1.text
            dwnpath = l2.text
            print(url, dwnpath)
            self.manobj.new(url, dwnpath)
            pop.dismiss()
            self.sm.current = 'single_dwnload'
            self.sm.current = 'main'
        
        pop = Popup(size_hint=(.8, .4), size=(500, 100))
        layout_s1 = BoxLayout(orientation='vertical', size_hint=(1,1))
        layout_s11 = BoxLayout(orientation='horizontal', size_hint=(1,.2))
        fc = FileChooserListView()
        l1 = Label(text='', size_hint=(.7, .8))
        b1 = Button(text='Choose', size_hint=(.3, .8))
        b1.bind(on_release=path_sel)
        layout_s11.add_widget(l1)
        layout_s11.add_widget(b1)
        layout_s1.add_widget(fc)
        layout_s1.add_widget(layout_s11)
        fc_pop = Popup(title = 'File Chooser', content=layout_s1, size_hint=(.8, .6), size=(500, 100))
        
        layout1 = BoxLayout(orientation='vertical')
        layout11 = BoxLayout(orientation='horizontal', size_hint=(1, .3))
        layout12 = BoxLayout(orientation='horizontal', size_hint=(1, .3))
        layout13 = BoxLayout(orientation='horizontal', size_hint=(1, .4))
        
        layout11.add_widget(Label(text='URL', size_hint=(.2, .6)))
        ti1 = TextInput(size_hint=(.6, .6))
        layout11.add_widget(ti1)
        layout11.add_widget(Label(text='', size_hint=(.07, .6)))
        layout12.add_widget(Label(text='DOWNLOAD PATH', size_hint=(.2, .6)))
        layout12.add_widget(Button(text='Browse', size_hint=(.1, .6),on_press = fc_pop.open))
        l2 = Label(text=fc.path, size_hint=(.57, .6))
        layout12.add_widget(l2)
        layout13.add_widget(Button(text='DOWNLOAD',size_hint=(.4, .6), on_press=dwnload))
        layout13.add_widget(Button(text='CANCEL',size_hint=(.4, .6), on_press=pop.dismiss))
        
        layout1.add_widget(layout11)
        layout1.add_widget(layout12)
        layout1.add_widget(layout13)
        pop.title = 'NEW DOWNLOAD'
        pop.content = layout1
        pop.open()
    
    def join(self, btn):
        
        def dwnload(btn):
            code = ti1.text
            print(code)
            self.manobj.join(code)
            self.sm.current = 'main'
        
        pop = Popup(size_hint=(.8, .4), size=(500, 100))
        layout1 = BoxLayout(orientation='vertical')
        layout11 = BoxLayout(orientation='horizontal', size_hint=(1, .3))
        layout12 = BoxLayout(orientation='horizontal', size_hint=(1, .3))
        layout13 = BoxLayout(orientation='horizontal', size_hint=(1, .4))
        
        layout11.add_widget(Label(text='CODE', size_hint=(.2, .6)))
        ti1 = TextInput(size_hint=(.6, .6))
        layout11.add_widget(ti1)
        layout11.add_widget(Label(text='', size_hint=(.07, .6)))
        layout13.add_widget(Button(text='DOWNLOAD',size_hint=(.4, .6), on_press=dwnload))
        layout13.add_widget(Button(text='CANCEL',size_hint=(.4, .6), on_press=pop.dismiss))
        
        layout1.add_widget(layout11)
        layout1.add_widget(layout12)
        layout1.add_widget(layout13)
        pop.title = 'JOIN DOWNLOAD'
        pop.content = layout1
        pop.open()
    
def font_size(width, height):
    print(width,height)    
if __name__=="__main__":
    Window.size = (790,610)
    Window.on_resize = font_size
    obj = BlueFangApp()
    obj.run()