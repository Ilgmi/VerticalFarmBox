(define (domain secSystemDomain)

(:requirements :strips :fluents :typing :conditional-effects :negative-preconditions :equality)

;types

(:types
    person time - object
    buzzer - actuator
    actuator - component
    algorithm - component
)

;predicates

(:predicates
    (is-on ?c - component)
    (is-recognized ?p - person)
    (has-waited ?time - time)
)

;actions

(:action turn-actuator-on
    :parameters (?a - actuator ?p - person ?t - time)
    :precondition (and (not (is-on ?a)) (is-recognized ?p) (not (has-waited ?t)) )
    :effect (and (is-on ?a))
)

(:action turn-actuator-off
    :parameters (?act - actuator ?time - time)
    :precondition (and (is-on ?act) (has-waited ?time) )
    :effect (and (not (is-on ?act)))
)

(:action wait-for-while
    :parameters ( ?person - person ?buzz - buzzer ?time - time)
    :precondition (and
       (not (has-waited ?time))
       (is-recognized ?person)
       (is-on ?buzz)
    )
    :effect (and
    (has-waited ?time)
    )
)

(:action wait-for-person
    :parameters (?person - person)
    :precondition (and (not (is-recognized ?person)))
    :effect (and (is-recognized ?person))
)

)