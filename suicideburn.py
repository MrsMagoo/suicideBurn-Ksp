import krpc, time, numpy
conn = krpc.connect(name="meuBurnkill")
vessel = conn.space_center.active_vessel
body = vessel.orbit.body
flight = vessel.flight(vessel.orbit.body.reference_frame)
control = vessel.control
#streams
altura = conn.add_stream(getattr, flight, 'surface_altitude')
velocidade = conn.add_stream(getattr, flight, 'speed')
horizontal = conn.add_stream(getattr, flight, 'horizontal_speed')
massa = conn.add_stream(getattr, vessel, 'mass')
thrust = conn.add_stream(getattr, vessel, 'thrust')
thrust_ainda = conn.add_stream(getattr, vessel, 'available_thrust')
max_thrust = conn.add_stream(getattr, vessel, 'max_thrust')
situacao = conn.add_stream(getattr, vessel, 'situation')
gravidade = conn.add_stream(getattr, body, 'surface_gravity')
elevacao = conn.add_stream(getattr, flight, 'elevation')
terminal_velocity = conn.add_stream(getattr, flight, 'terminal_velocity')
#outras...
pouso = False
pousado_agua = conn.space_center.VesselSituation.splashed
pousado = conn.space_center.VesselSituation.landed
velo_atual = velocidade()
motor = thrust()/massa()
aceleracao = motor - gravidade()
def throttle(valor):
    vessel.control.throttle = valor
altura_atual = altura()
while altura_atual > 18000:
    altura_atual = altura()
    print("esperando time do burn")
    time.sleep(2)
print('BURN')
throttle(0)
vessel.control.breakes = True
vessel.control.gears = True
time.sleep(0.5)
velo_atual = velocidade()
#inicio do burn
if situacao() == pousado_agua:
    pouso = True
elif situacao() == pousado:
    pouso = True
while pouso == False:
    if situacao() == pousado_agua:
        pouso = True
    elif situacao() == pousado:
        pouso = True
    vessel.control.breakes = True
    vessel.control.gears = True
    altura_atual = altura() #6 nesta nave
    velo_atual = velocidade()
    acel_1 = max_thrust() / massa()
    aceleracao = acel_1 - gravidade()
    teste = abs((velo_atual ** 2) / ( 3 * aceleracao))
    #erro = (terminal_velocity() * ( (massa())  / 10000 ))
    #erro = (impulso() - 170 ) # 180 deu boa
    erro = (velocidade())
    '''# / 10000) ) # grande 10000 '''
    dis_burn = (teste + erro + 70)  #aparenta q o 70 é a altura q ele quase termina o suicide, aonde comeca a atuar os if's de pouso suave
    #variavel q na nave grande seja igual a +ou= 160 ***
    print('altura atual: %2.f' % (altura_atual))
    print('altura burn: %2.f' % (dis_burn))
    print('velocidade: %2.f' % (velo_atual))
    vessel.control.sas = True
    if altura_atual > 150 and velo_atual > 50 :
        vessel.control.sas_mode = conn.space_center.SASMode.retrograde
    elif altura_atual < 90 and velo_atual < 50:
        vessel.control.sas_mode = conn.space_center.SASMode.radial
        vessel.control.rcs = True
    #ajuda entre 3000 e 2000 metros
    '''
    if altura_atual < 3000 and altura_atual > 2000 and velo_atual > 200:
        throttle(0.7)
    if altura_atual < 3000 and altura_atual> 2000 and velo_atual < 200:
        throttle(0) '''
    if velo_atual < 4:
        throttle(0.1)
    if altura_atual < dis_burn and  velo_atual > 15 and altura_atual > 50:
        throttle(1)
    if altura_atual > dis_burn and altura_atual > 2000:
        throttle(0)
    if altura_atual < dis_burn and velo_atual < 15 and altura_atual > 50:
        throttle(0.5)
    if altura_atual < 50 and velo_atual > 10 and altura_atual > 30 :
        throttle(1)
    if altura_atual < 30 and velo_atual > 15:
        throttle(1)
    if altura_atual < 30 and velo_atual < 10 and velo_atual > 6:
        throttle(0.6)
    elif velo_atual < 5 and velo_atual > 3:
        throttle(0.3)
    elif velo_atual < 3:
        throttle(0.1)

    #if pousado == True:
        #vessel.control.throttle = 0
    time.sleep(0.1)
throttle(0)
time.sleep(2)
vessel.control.sas_mode = conn.space_center.SASMode.stability_assist
print('TOUCHDOW!!!!!')
