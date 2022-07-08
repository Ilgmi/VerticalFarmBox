(define (problem secSystemProblem)

(:domain secSystemDomain)
(:objects
	buzzerObj - buzzer
    burglar - person
    timeObj - time
    algorithmObj - algorithm

)

(:init
    (is-on algorithmObj)
)

(:goal (and
    (not (is-on buzzerObj))
    (is-recognized burglar)
    (has-waited timeObj)
    (is-on algorithmObj)
))

)