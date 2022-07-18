import {Plant} from './plant';
import {Condition} from './condition';

export interface GreenhouseBox {
  _id: string
  key: string
  building: string
  room: string
  name: string
  connection_state: boolean
  created: Date
  updated: Date

  roof : number
  water_pump : number
  show_text : number
  watering_plants : number
  temperature : number
  humidity : number
  light : number
  plant: Plant

  temperature_condition: Condition
  humidity_condition: Condition
  
}
