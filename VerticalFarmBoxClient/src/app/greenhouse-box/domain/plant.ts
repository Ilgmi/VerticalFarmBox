export enum MoistureLevel {
  dry = 0,
  wet = 1,
  very_wet = 2
}

export interface Plant {
  moisture_level: MoistureLevel
}
