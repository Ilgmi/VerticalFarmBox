(define (problem plantfarm) (:domain smartPlantFarm)
(:objects
    t0 - temperature
    h0 - humidity 
    m0 - moisture
    l0 - light 
    r0 - roof 
    p0 - pump 
    d0 - display 
)

(:init 
    (is_pump_off ?p - pump)
    (is_temp_down ?t - temperature)
    (is_hum_down ?h - humidity)
    (is_soil_dry ?s - moisture)
    (is_light_opt ?l - light)
    (is_roof_close ?r -roof)
    (is_change_water_text_not_shown ?d - display)
    
    ;definiton 
    (= (min_temperature) $$min_temperature$$)
    (= (max_temperature $$max_temperature$$)
    
    (= (min_humidity) $$min_humidity$$)
    (= (max_humidity) $$max_humidity$$)
    
    (= (watering_count) $$watering_count$$)
    (= (max_watering_count) $$max_watering_count$$)

    (= (actual_temp) ?t $$actual_temp$$)
    (= (actual_hum) ?h $$actual_hum$$)
)

(:goal (and
        (is_pump_on ?p - pump)
        (is_roof_open ?r -roof)
        (is_change_water_text_shown ?d - display)
        )
)













)