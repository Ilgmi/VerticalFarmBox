(define (domain smartPlantFarm)

    (:requirements
        :strips
        :typing
        :equality
        :negative-preconditions
        
        
    )

    (:types
        box temperature humidity moisture light roof pump display

    )
    
    (:predicates
    
    ;water pump is operational and ready 
    (is_pump_on ?p - pump)
    (is_pump_off ?p - pump)
    
    ;temperature up/down from the optimal value 
    (is_temp_up ?t - temperature)
    (is_temp_down ?t - temperature)
    
    ;humidity up/dowm from the optimal value 
    (is_hum_up ?h - humidity)
    (is_hum_down ?h - humidity)
    
    ;light high, optimal, low 
    (is_light_high ?l - light)
    (is_light_opt ?l - light)
    (is_light_low ?l - light)
    
    ;moisture (soil is dry/wet), is in water 
    (is_soil_dry ?s - moisture)
    (is_soil_wet ?s - moisture)
    
    ;roof (open/close)
    (is_roof_open ?r - roof)
    (is_roof_close ?r -roof)
 
    (is_change_water_text_shown ?d - display)
    (is_change_water_text_not_shown ?d - display)

    (is_done ?b - box)
    
    )

    (:functions
    
    (actual_temp ?t - temperature)
    (actual_hum ?h - humidity)
  
    (min_temperature)
    (max_temperature)
    
    (min_humidity)
    (max_humidity)
    
    
    (actual_lightlevel ?l - light)
    (wantedLightlevel)
    
    (watering_count)
    (max_watering_count)
    
    )
    
    ;water pump is on 
    (:action pump_on 
        :parameters (?p - pump ?s - moisture)
        :precondition (and 
                        (is_pump_off ?p)
                        (is_soil_dry ?s)
                    )
        :effect (and 
                    (is_pump_on ?p)
                    (not (is_pump_off ?p))
                )
    )
    
    ;water pump is off 
    (:action pump_off 
        :parameters (?p - pump ?s - moisture)
        :precondition (and 
                        (is_pump_on ?p)
                        (is_soil_wet ?s)
                    )
        :effect (and 
                    (is_pump_off ?p)
                    (not (is_pump_on ?p))
                )
    )
    
    ;open the roof 
    (:action open_roof
        :parameters (?r - roof ?t - temperature ?h - humidity)
        :precondition (and 
                        (is_roof_close ?r)
                        
                        (or (and
                            (> (actual_temp ?t) (max_temperature))
                            )
                            (and 
                            (> (actual_hum ?h) (max_humidity))
                            )
                        )
                    )
        :effect (and 
                    (is_roof_open ?r)
                    (not (is_roof_close ?r))
                )
    )
    
    ;close the roof 
    (:action close_roof 
        :parameters (?r - roof ?t - temperature ?h - humidity)
        :precondition (and 
                        (is_roof_open ?r)
                        
                        (or (and
                            (< (actual_temp ?t) (min_temperature))
                            )
                            (and 
                            (< (actual_hum ?h) (min_humidity))
                            )
                        )
                    )
        :effect (and 
                    (is_roof_close ?r)
                    (not (is_roof_open ?r))
                )
    )

    ;close the roof
    (:action do_nothing
        :parameters (?b - box ?r - roof ?t - temperature ?h - humidity)
        :precondition (and
                        (> (actual_temp ?t) (min_temperature))
                        (< (actual_temp ?t) (max_temperature))

                        (> (actual_hum ?h) (min_humidity))
                        (< (actual_hum ?h) (max_humidity))
                    )
        :effect (and
                    (is_done ?b)
                )
    )
    
    (:action show_change_water_text 
        :parameters (?d - display)
        :precondition (and 
                        (is_change_water_text_not_shown ?d)
                        (> (watering_count) (max_watering_count))
                        
                    )
        :effect (and 
                    (is_change_water_text_shown ?d)
                    (not (is_change_water_text_not_shown ?d))
                )
    )
    
    (:action do_not_show_change_water_text 
        :parameters (?d - display)
        :precondition (and 
                        (is_change_water_text_shown ?d)
                        (< (watering_count) (max_watering_count))

                    )
        :effect (and 
                    (is_change_water_text_not_shown ?d)
                    (not (is_change_water_text_shown ?d))
                )
    )
    
    
)