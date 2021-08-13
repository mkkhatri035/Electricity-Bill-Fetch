from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import PySimpleGUI as sg



states=['select state']


site='https://www.freecharge.in/electricity'

## freecharge electricity bill check



def freechargeelectricity(state,elc_provdr,cano): 
    driver.get(site)
    time.sleep(3)
    print(elc_provdr)
    s=driver.find_element_by_css_selector('body.pace-done:nth-child(2) div.main div.container div.main-container div.main-container-component:nth-child(3) div.not-logged div._1vt0D div.FFYy9:nth-child(2) div._2U5N8 div.select-container._1Qgtu > select:nth-child(1)')
    st=Select(s)
    st.select_by_value(state)

    time.sleep(2)
    s=driver.find_element_by_css_selector('body.pace-done:nth-child(2) div.main div.container div.main-container div.main-container-component:nth-child(3) div.not-logged div._1vt0D div.FFYy9:nth-child(3) div._2U5N8 div.select-container._1Qgtu > select:nth-child(1)')
    sp=Select(s)
    sp.select_by_visible_text(elc_provdr)

    driver.execute_script('''document.querySelector("input[name='consent']").checked=false''')

    time.sleep(2)
    s=driver.find_element_by_css_selector('body.pace-done:nth-child(2) div.main div.container div.main-container div.main-container-component:nth-child(3) div.not-logged div._2D867._1vt0D div.fxO_s._3msNg:nth-child(5) form:nth-child(1) div.c9oVh div.input-container.undefined._2HmRw.false > input:nth-child(1)')
    s.send_keys(cano)

    btn=driver.find_element_by_class_name('_1H40I')
    btn.click()
    time.sleep(3)
    eles=driver.find_elements_by_class_name('_2xM4c')
    return [i.text for i in eles]


def getstat():
    ele=driver.find_element_by_class_name('_1Qgtu')
    temp=ele.text.split('\n')
    temp.pop(0)
    states.extend(temp)



def getelec(sta):
    ele=driver.find_element_by_class_name('_1Qgtu')
    ee=Select(ele.find_element_by_xpath('//select'))
    ee.select_by_visible_text(sta)
    eles=driver.find_elements_by_class_name('_1Qgtu')
    temp=eles[1].text.split('\n')
    return  temp


def guitake():
    getstat()
    
    lay=[[sg.Text('Your State'),sg.Text('',size=(7,1)),sg.InputCombo(states,default_value='select state',key='stat',enable_events=True)],
         [sg.Text('Your electricity provide'),sg.InputCombo(['Electricity Provider'],default_value='Electricity Provider',key='elp')],
         [sg.Text('Your CA No'),sg.Text('',size=(6,1)),sg.Input('',key='cano')],
         [sg.Button('Get Bill Amount')]
         ]
    
    window=sg.Window(title='Bill Checker', layout=lay)
    while True:
        event,values=window.read()
        if(event==sg.WIN_CLOSED or event=='Exit'):
            break
        if(window['stat'].get()!='select state' and window['elp'].get()=='Electricity Provider'):
            window['elp'].Update(values=getelec(window['stat'].get()),set_to_index=0)
        if(event=='Get Bill Amount'):
            if(window['stat'].get()!=states[0] and window['elp'].get()!='Electricity Provider' and window['cano'].get()!=''):
                lis=freechargeelectricity(window['stat'].get(),window['elp'].get(),window['cano'].get())
                l=[[sg.Text('Bill',size=(30,2))]]
                for i in lis :
                   n=i.split('\n')
                   n.append('')
                   l.append([sg.Text(n[0],size=(15,1)),sg.Text(n[1],size=(15,1))])
                l.append([sg.Button('Ok',size=(15,2))])
                wind=sg.Window('bill',layout=l)
                window.disappear()
                e,v=wind.read()
                if e in ('Close',sg.WIN_CLOSED,'Ok'):
                   wind.close()
                   window.reappear()
                
                     

if(__name__=='__main__'):
    driver=webdriver.Firefox(executable_path='geckodriver')
    driver.get( site)
    time.sleep(2)
    guitake()
