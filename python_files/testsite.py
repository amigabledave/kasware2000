class KSU():
	next_critical_burn = None


next_event = 'Siguiente evento'
ksu = KSU()


next_critical_burn = ksu.next_critical_burn
if not ksu.next_critical_burn:
	next_critical_burn = next_event
	ksu.next_critical_burn = next_event	

print ksu.next_critical_burn


