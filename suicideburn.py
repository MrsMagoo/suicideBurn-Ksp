import krpc, time
from math import *

conn = krpc.connect(name='suicidio')
###--- Variaveis principais ---###
vessel = conn.space_center.active_vessel
body =  vessel.orbit.body
flight = vessel.flight(vessel.orbit.body.reference_frame)
control = vessel.control
###--- variaveis para os calculos ---###
vel_vertical = conn.add_stream(getattr, flight, 'vertical_speed')
max_thrust = sum(e.max_thrust for e in vessel.parts.engines)
mass = conn.add_stream(getattr, vessel, 'mass')
massa_seca = conn.add_stream(getattr, vessel, 'dry_mass')
forcag = conn.add_stream(getattr, flight, 'g_force')
altitude = conn.add_stream(getattr, flight, 'surface_altitude')
aceleracao_gravidade = conn.add_stream(getattr, body, 'surface_gravity')
impulso = conn.add_stream(getattr, vessel, 'specific_impulse')
thrust_avaliavel = conn.add_stream(getattr, vessel, 'available_thrust')
###--- variaveis de situacao --###
pousado_agua = conn.space_center.VesselSituation.splashed
pousado = conn.space_center.VesselSituation.landed
###--- Variaveis calculadas ---###
naveDeltaV = log(mass() / massa_seca()) * impulso()* aceleracao_gravidade()
taxaDeQueima = thrust_avaliavel() / (impulso() * aceleracao_gravidade());
TWR = thrust_avaliavel() / (mass() * aceleracao_gravidade());
aceleracao = 1
### Ligando SAS ###
vessel.control.sas = True
vessel.control.sas_mode = conn.space_center.SASMode.radial

distancia = (vel_vertical() * vel_vertical()) / (2 * max_thrust)
###--- Funcoes pra facilitar ---###
def throttle_d(valor):
    vessel.control.throttle = valor
###-- Variaveis pra testes ---##
verdade = True
erro = 100
teste = 30
corecao_aceleracao = 0
### loop pra fazer o suicideburn ###
while vessel.situation == conn.space_center.VesselSituation.flying:
    corecao_aceleracao = abs(log((sqrt(aceleracao / ((naveDeltaV / taxaDeQueima) ** 2) * TWR))))
    aceleracao = (corecao_aceleracao * 0.95 / TWR)
    throttle_d(aceleracao)
        #corecao_aceleracao = abs(log((sqrt(aceleracao / ((naveDeltaV / taxaDeQueima) ** 2) * TWR))))
        #correcaoAceleracao = Math.abs(Math.log(Math.abs(Math.sqrt(Math.abs + (aceleracao / ((naveDeltaV * Math.abs(tempoDeQueima)) * (taxaDeQueima) / naveTWR))))));

    print(corecao_aceleracao)
    print(aceleracao)
        ###planando (funcionando))
    '''
            alt_error = erro - altitude()
            throttle = (mass() * (forcag() - vel_vertical() + alt_error)) / max_thrust
            throttle = max(min(1, throttle), 0)
            control.throttle = throttle
            erro = erro - 0.5 '''


        #print('%.2f\r' % altitude())
        #time.sleep(0.2)
        #teste = teste - 1
if vessel.situation != conn.space_center.VesselSituation.flying:
    throttle_d(0)
    #corecao_aceleracao = abs(math.log((math.sqrt(aceleracao / ((naveDeltaV / taxaDeQueima)** 2) * TWR))))
    #print(corecao_aceleracao)
'''
while verdade == True :
    situacao = vessel.situation
    distancia = (vel_vertical() * vel_vertical()) / (2 * max_thrust)
    novaac = (1/max_thrust + distancia)
    print(novaac)
    if situacao == pousado or situacao == pousado_agua:
        verdade = False
#while True:
 #   alturaPouso = '''
'''
    while True: ## {// LOOP PRINCIPAL DE SUICIDE BURN
     ### atualizarVariaveis(); // atualiza valores
    ##// -= - Informa ao PID a altitude da nave e o limite -= -
    controleAcel.setValorLimite(alturaPouso + distanciaDaQueima);

    if flight.surface_altitude < 50: #// altitude para as perninhas
        vessel.control.gear = True '''
    #-= - Corrigir a aceleracao -= -
    #distancia = (vel_vertical() * vel_vertical()) / (2 * max_thrust)
    #novaAcel = (1 / max_thrust + distancia());
    #throttle(novaAcel)
    #naveAtual.getControl().setThrottle(novaAcel);
    #Thread.sleep(10);

##} // Fim loop -while

#### conta
'''
distancia = (vel_vertical() * vel_vertical()) / (2 * max_thrust)

'''