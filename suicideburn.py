import krpc, time
from math import *

conn = krpc.connect(name='suicidio')
###--- Variaveis principais ---###
vessel = conn.space_center.active_vessel
body =  vessel.orbit.body
flight = vessel.flight(vessel.orbit.body.reference_frame)
control = vessel.control
###--- variaveis para os calculos ---###
altura = conn.add_stream(getattr, flight, 'surface_altitude')
velocidade = conn.add_stream(getattr, flight, 'speed')
massa = conn.add_stream(getattr, vessel, 'mass')
thrust = conn.add_stream(getattr, vessel, 'thrust')
thrust_ainda = conn.add_stream(getattr, vessel, 'available_thrust')
max_thrust = conn.add_stream(getattr, vessel, 'max_thrust')
situacao = conn.add_stream(getattr, vessel, 'situation')
gravidade = conn.add_stream(getattr, body, 'surface_gravity')
pouso = False
pousado_agua = conn.space_center.VesselSituation.splashed
pousado = conn.space_center.VesselSituation.landed
velo_atual = velocidade()
motor = thrust()/massa()
aceleracao = motor - gravidade()
#Funcao pra forca do motor
def throttle(valor):
    vessel.control.throttle = valor
altura_atual = altura()
#altura inicial pra comecar a calcular o burn
while altura_atual > 10000:
    altura_atual = altura()
    print("esperando time do burn")
    time.sleep(2)
print('BURN')
vessel.control.breakes = True
vessel.control.gears = True
time.sleep(0.5)
velo_atual = velocidade()
#so pra nao ligar os motores se estiver pousado
if situacao() == pousado_agua:
    pouso = True
elif situacao() == pousado:
    pouso = True
#inicio da contagem do burn
while pouso == False:
    if situacao() == pousado_agua:
        pouso = True
    elif situacao() == pousado:
        pouso = True
    vessel.control.breakes = True
    vessel.control.gears = True
    altura_atual = altura() #6 nesta nave
    velo_atual = velocidade()
    motor = thrust_ainda() / massa()
    aceleracao = motor - gravidade()
    teste = abs((velo_atual ** 2) / ( 2.5 * aceleracao))
    dis_burn = (teste + 100)
    #mostrando informacoes no console
    print('altura atual: %2.f' % (altura_atual))
    print('altura burn: %2.f' % (dis_burn))
    print('velocidade: %2.f' % (velo_atual))
    # pra pousar com calma HEHE
    if altura_atual < dis_burn and  velo_atual > 12 and altura_atual > 50:
        throttle(1)
    if altura_atual < 50 and velo_atual < 12 and velo_atual > 5:
        throttle(0.8)
    elif velo_atual < 5:
        throttle(0.2)
    time.sleep(0.1)
throttle(0)
print('pousado com sucesso, espero')
