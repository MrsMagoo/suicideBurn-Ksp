# -*- coding: utf-8 -*-
import krpc, time
conn = krpc.connect(name="meuBurnkill")
vessel = conn.space_center.active_vessel
body = vessel.orbit.body
flight = vessel.flight(vessel.orbit.body.reference_frame)
control = vessel.control
altura = conn.add_stream(getattr, flight, 'surface_altitude')
velocidade = conn.add_stream(getattr, flight, 'speed')
horizontal = conn.add_stream(getattr, flight, 'horizontal_speed')
vertical = conn.add_stream(getattr, flight, 'vertical_speed')
massa = conn.add_stream(getattr, vessel, 'mass')
thrust = conn.add_stream(getattr, vessel, 'thrust')
thrust_ainda = conn.add_stream(getattr, vessel, 'available_thrust')
max_thrust = conn.add_stream(getattr, vessel, 'max_thrust')
situacao = conn.add_stream(getattr, vessel, 'situation')
gravidade = conn.add_stream(getattr, body, 'surface_gravity')
elevacao = conn.add_stream(getattr, flight, 'elevation')
terminal_velocity = conn.add_stream(getattr, flight, 'terminal_velocity')
impulso = conn.add_stream(getattr, vessel, 'kerbin_sea_level_specific_impulse')
pouso = False
pousado_agua = conn.space_center.VesselSituation.splashed
pousado = conn.space_center.VesselSituation.landed
velo_atual = velocidade()
motor = thrust()/massa()
aceleracao = motor - gravidade()
def throttle(valor):
    vessel.control.throttle = valor
altura_atual = altura()
#janela
canvas = conn.ui.stock_canvas
screen_size = canvas.rect_transform.size
panel = canvas.add_panel()
rect = panel.rect_transform
rect.size = (190, 130)
rect.position = (95-(screen_size[0]/2), 285)
#textos
textaltura = panel.add_text("altura: 0 M")
textaltura.rect_transform.position = (0, -36)
textaltura.color = (1, 1, 1)
textaltura.size = 18
#texto de informacoes
text = panel.add_text('vel.vet: 0 m/s')
text.rect_transform.position = (0, -15)
text.color = (1, 1, 1)
text.size = 18
#testo burn
textoburn = panel.add_text('SuicideBurn OFF')
textoburn.rect_transform.position = (0, -54)
textoburn.color = (1, 1, 1)
textoburn.size = 18
# adicionando botao, pra comecar o suicide
button = panel.add_button("Suicide Burn")
button_clicked = conn.add_stream(getattr, button, 'clicked')
button.rect_transform.position = (0, 35)

while True:
    # Update textos
    text.content = 'Thrust: %d kN' % (vessel.thrust / 1000)
    textaltura.content = 'Altura: %1.f' % (altura())
    if situacao() != pousado_agua:
        pouso = False
    elif situacao() != pousado:
        pouso = False
    #BOTAO AQUI
    if button_clicked():
    #if True: #tirar
        button.clicked = False
        textoburn.content = ('altura burn: calculando...')
        while altura_atual > 7000:
            text.content = 'Thrust: %d kN' % (vessel.thrust / 1000)
            textaltura.content = 'Altura: %1.f' % (altura())
            textoburn.content = ('altura burn: Calculando...')
            if altura_atual <= 16000 and altura_atual > 1000:
                contagem = 1
                vessel.control.brakes = True
                if contagem == 1 :
                    print('abrindo brakes')
                    contagem = - 1
                    time.sleep(1)
            altura_atual = altura()
            print("esperando time do burn")
            time.sleep(2)
        time.sleep(2)
        print('iniciando calculos')
        throttle(0)
        time.sleep(0.5)
        vessel.control.brakes = True
        #inicio do burn
        while pouso == False:

            if situacao() == pousado_agua:
                pouso = True
            elif situacao() == pousado:
                pouso = True
            altura_atual = (altura() + 10) #margem de erro da altura
            velo = velocidade()
            velo_atual = velocidade() + 3.5 # 3.5 relacao com aceleracao era boa
            acel_1 = thrust_ainda() / massa()
            acel_2 = max_thrust() / (massa() * gravidade())
            aceleracao = acel_1 - gravidade()
            teste = abs((velo_atual ** 2) / ( 3 * aceleracao))
            #teste = abs(velo_atual / acel_1)
            #erro = (terminal_velocity() * ( (massa())  / 10000 ))
            #erro = (impulso() - 170 ) # 180 deu boa
            TWR = max_thrust() / (massa() * gravidade())
            aceleracao_max = (TWR * gravidade()) - gravidade()
            tempo = vertical() / aceleracao_max
            distancia = abs(velocidade() *(  tempo / 2.3 ) ) # +  1/3 * aceleracao_max * (tempo))
            print('distancia:', distancia)
            print('teste:', teste)
            erro = (160)
            '''# / 10000) ) # grande 10000 '''
            #dis_burn = (teste + erro) #NAVE GRANDE 160 funcionando com nave pequena( gracas aos if de velocidade )
            dis_burn = (distancia)
            #variavel q na nave grande seja igual a +ou= 160 ***
            #print('altura atual: %2.f' % (altura_atual))
            #print('altura burn: %2.f' % (dis_burn))
            #print('velocidade: %2.f' % (velo))
            vessel.control.sas = True
            if altura_atual > 60 and velo > 50 :
                vessel.control.sas_mode = conn.space_center.SASMode.retrograde
            elif altura_atual < 60 and velo < 50:
                vessel.control.sas_mode = conn.space_center.SASMode.radial
                vessel.control.rcs = True
            if horizontal() > 2:
                vessel.control.sas_mode = conn.space_center.SASMode.retrograde
            #ajuda entre 3000 e 2000 metros
            '''
            if altura_atual < 3000 and altura_atual > 2000 and velo_atual > 200:
            throttle(0.7)
            if altura_atual < 3000 and altura_atual> 2000 and velo_atual < 200:
            throttle(0) '''
            ligado = 0
            if velo < 4 and altura_atual > 100:
                throttle(0.1)
            if velocidade > 10  and velocidade < 40 and altura_atual > 100 and altura_atual < 500:
                throttle(0.01)
            if altura_atual < dis_burn and  velo > 15 and altura_atual > 50:
                throttle(1)
                ligado = 1
            if altura_atual <= 600 and velo_atual <= 150:
                vessel.control.brakes = False
            if ligado == 1 and altura_atual > dis_burn  :
                throttle(0.2)
            if altura_atual < dis_burn and velo < 15 and altura_atual > 50:
                throttle(0.5)
            if altura_atual < 50 and velo > 10 and altura_atual > 30 :
                throttle(1)
            if altura_atual < 30 and velo > 15:
                throttle(1)
            if altura_atual < 30 and velo < 10 and velo > 6:
                throttle(0.6)
            elif velo < 5 and velo > 3:
                throttle(0.3)
            elif velo < 3:
                throttle(0.1)
            if altura_atual < 1000:
                vessel.control.gear = True
            #if pousado == True:
                #vessel.control.throttle = 0
            #text.content = 'Thrust: %d kN' % (vessel.thrust / 1000)
            text.content = 'horizontal: %d kN' % (horizontal())
            textaltura.content = 'Altura: %1.f' % (altura())
            textoburn.content = ('altura burn: %2.f' % (dis_burn))
            time.sleep(0.1)
        throttle(0)
        time.sleep(1)
        vessel.control.sas_mode = conn.space_center.SASMode.stability_assist
        print('TOUCHDOW!!!!!')
        time.sleep(1)
        print('estabilizando')
        time.sleep(4)
        print('pouso terminado, desligando tudo, tchau!!')
        vessel.control.sas = False
        vessel.control.rcs = False
        vessel.control.brakes = False
