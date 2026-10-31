/** Search synonyms: what people say on the phone -> what the catalog calls it. */
export const SYNONYMS: Record<string, string[]> = {
  pawl: ['dog', 'paul', 'pall', 'locking bar', 'latch', 'catch'],
  solenoid: ['coil', 'plunger', 'actuator', 'electromagnet', 'magnet'],
  microswitch: ['micro switch', 'limit switch', 'roller switch', 'lever switch', 'sensor switch'],
  spring: ['springs', 'coil spring', 'return spring'],
  bearing: ['bushing', 'flange', 'pillow block', 'race'],
  shock: ['damper', 'dashpot', 'shock absorber', 'speed control', 'hydraulic'],
  board: ['controller', 'circuit board', 'pcb', 'logic board', 'brain', 'control board', 'main board'],
  plc: ['programmable', 'fp0', 'panasonic', 'nais', 'aromat'],
  relay: ['ice cube', 'contactor', 'timer relay'],
  counter: ['totalizer', 'register', 'odometer'],
  transformer: ['power supply', 'rectifier', 'psu'],
  lamp: ['light', 'led', 'indicator', 'bulb', 'arrow light'],
  'full height': ['full-height', 'fh', 'tall turnstile', 'stg'],
  'waist high': ['waist-high', 'wh', 'tripod', 'three arm', '3 arm'],
};
