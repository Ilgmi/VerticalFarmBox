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
    (= (min_temperature) 20)
    (= (max_temperature 30)
    
    (= (min_humidity) 60)
    (= (max_humidity) 80)
    
    (= (watering_count) 0) 
    (= (max_watering_count) 20) 
)

(:goal (and
        (is_pump_on ?p - pump)
        (is_roof_open ?r -roof)
        (is_change_water_text_shown ?d - display)
        )
)













)