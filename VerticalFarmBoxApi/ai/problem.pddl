(define (problem plantfarm) (:domain smartPlantFarm)
(:objects
    b0 - box
    t0 - temperature
    h0 - humidity 
    m0 - moisture
    l0 - light 
    r0 - roof 
    p0 - pump 
    d0 - display 
)

(:init

    ($$pump_state$$ p0)
    ($$roof_state$$ r0)

    ($$soil_state$$ m0)
    ($$show_text_state$$ d0)

    (is_light_opt l0)
    (not (output_done b0) )
    
    ;definiton 
    (= (min_temperature) $$min_temperature$$)
    (= (max_temperature) $$max_temperature$$)
    
    (= (min_humidity) $$min_humidity$$)
    (= (max_humidity) $$max_humidity$$)
    
    (= (watering_count) $$watering_count$$)
    (= (max_watering_count) $$max_watering_count$$)

    (= (actual_temp t0)  $$actual_temp$$)
    (= (actual_hum h0)  $$actual_hum$$)
)

(:goal (or
        ($$pump_state_goal$$ p0)
        ($$roof_state_goal$$ r0)
        ($$show_text_state_goal$$ d0)
        (is_done b0)
        )
)













)