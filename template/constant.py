import os
from PIL import Image

URL_ROOT    = "https://prod.chronolife.net/api/2"
URL_DATA    = URL_ROOT + "/data"
URL_USER    = URL_ROOT + "/user"

TYPE = {}
TYPE_ECG                 = "ecg"
TYPE_BREATH_THORACIC     = "breath_1"
TYPE_BREATH_ABDOMINAL    = "breath_2"
TYPE_ACCELERATION_X      = "accx"
TYPE_ACCELERATION_Y      = "accy"
TYPE_ACCELERATION_Z      = "accz"
TYPE_RAW_SIGNALS        = (TYPE_ACCELERATION_X + "," + 
                                           TYPE_ACCELERATION_Y + "," + 
                                           TYPE_ACCELERATION_Z +','  +
                                           TYPE_ECG + "," + 
                                           TYPE_BREATH_THORACIC + "," +
                                           TYPE_BREATH_ABDOMINAL)
TYPE_FILTERED_SIGNALS   = (TYPE_ECG + "," + 
                                           TYPE_BREATH_THORACIC + "," +
                                           TYPE_BREATH_ABDOMINAL)
TYPE_SIGNALS            = (TYPE_RAW_SIGNALS + "," + 
                                           TYPE_FILTERED_SIGNALS)
TYPE_HEARTBEAT          = "heartbeat"
TYPE_INDICATORS         = (TYPE_HEARTBEAT)

CURRENT_DIRECTORY = os.getcwd()
QC_TIMER = 15

LOGO_CLIFE = Image.open(CURRENT_DIRECTORY + '/assets/logoclife.png')

COLORS = {}
COLORS["text"]          = '#3E738D'
COLORS["garmin"]        = "#6CCFF6"
COLORS["chronolife"]    = "#F7921E"
COLORS["acc"]           = "#6BA439"
COLORS["acc_2"]         = "#71c924"
COLORS["acc_3"]         = "#74f007"
COLORS["ecg"]           = "#A2407E"
COLORS["breath"]        = "#3C7290" #97CCDB"
COLORS["breath_2"]      = "#51C3CA"
COLORS["temp"]          = "#FF9300"
COLORS["temp_2"]        = "#ff6a00"

COLORS['stress']        = "#FF9300"
COLORS['stress_rest']   = "#4594F3"
COLORS['stress_low']    = "#FFAF54"
COLORS['stress_medium'] = "#F97516"
COLORS['stress_high']   = "#DD5809"

COLORS['sleep']         = "#A2407E"
COLORS['sleep_deep']    = "#044A9A"
COLORS['sleep_light']   = "#1878CF"
COLORS['sleep_rem']     = "#9D0FB1"
COLORS['sleep_awake']   = "#EB79D2"

COLORS['spo2']          = "#6BA439"
COLORS['spo2_green']    = "#17A444"
COLORS['spo2_low']      = "#F8CB4B"
COLORS['spo2_medium']   = "#F77517"
COLORS['spo2_high']     = "#CE4A14"

COLORS['pulseox']       = "#6BA439"
COLORS['bodybattery']   = "#51C3CA"

COLORS['bpm']           = COLORS["ecg"]
COLORS['sdnn']          = COLORS["ecg"]
COLORS['hrv']           = COLORS["ecg"]
COLORS['tachycardia']   = COLORS["ecg"]
COLORS['bradycardia']   = COLORS["ecg"]
COLORS['qt']            = COLORS["ecg"]
COLORS['brpm']          = COLORS["breath"]
COLORS['rpm_1']         = COLORS["breath"]
COLORS['brv_1']         = COLORS["breath"]
COLORS['rpm_2']         = COLORS["breath_2"]
COLORS['brv_2']         = COLORS["breath_2"]
COLORS['bior_1']        = COLORS["breath"]
COLORS['bior_2']        = COLORS["breath_2"]
COLORS['tachypnea_1']   = COLORS["breath"]
COLORS['bradypnea_1']   = COLORS["breath"]
COLORS['tachypnea_2']   = COLORS["breath_2"]
COLORS['bradypnea_2']   = COLORS["breath_2"]
# COLORS['bior'] = '%'

SHORTCUT = {}
SHORTCUT['bpm'] = 'Heart Beat Per Minute (BPM)'
SHORTCUT['sdnn'] = 'Heart Rate Variability (SDRR)'
SHORTCUT['hrv'] = 'Heart Rate Variability (SDRR)'
SHORTCUT['tachycardia'] = 'Tachycardia'
SHORTCUT['bradycardia'] = 'Bradycardia'
SHORTCUT['qt'] = 'QT length'
SHORTCUT['brpm'] = 'Breath Rate Per Minute (BRPM)'
SHORTCUT['rpm'] = 'Breath Rate Per Minute (BRPM)'
SHORTCUT['brv'] = 'Breath Rate Variability (BRV)'
SHORTCUT['bior'] = 'Inhalation exhalation length ratio'
SHORTCUT['tachypnea'] = 'Tachypnea'
SHORTCUT['bradypnea'] = 'Bradypnea'
SHORTCUT['rpm_1'] = 'Thoracic breath'
SHORTCUT['brv_1'] = 'Thoracic breath'
SHORTCUT['bior_1'] = 'Thoracic breath'
SHORTCUT['tachypnea_1'] = 'Thoracic breath'
SHORTCUT['bradypnea_1'] = 'Thoracic breath'
SHORTCUT['rpm_2'] = 'Abdominal breath'
SHORTCUT['brv_2'] = 'Abdominal breath'
SHORTCUT['bior_2'] = 'Abdominal breath'
SHORTCUT['tachypnea_2'] = 'Abdominal breath'
SHORTCUT['bradypnea_2'] = 'Abdominal breath'
SHORTCUT['temp'] = 'Skin Temperature'
SHORTCUT['n_steps'] = 'Step number'
SHORTCUT['stress'] = 'Stress score'
SHORTCUT['sleep'] = 'Sleep quality'
SHORTCUT['spo2'] = 'Oxygen saturation'
SHORTCUT['pulseox'] = 'Oxygen saturation'
SHORTCUT['bodybattery'] = 'Body Battery'

UNIT = {}
UNIT['bpm'] = 'bpm'
UNIT['sdnn'] = 'ms'
UNIT['hrv'] = 'ms'
UNIT['tachycardia'] = 'bpm'
UNIT['bradycardia'] = 'bpm'
UNIT['qt'] = 'ms'
UNIT['brpm'] = 'brpm'
UNIT['brv'] = 's'
UNIT['rpm_1'] = 'brpm'
UNIT['brv_1'] = 's'
UNIT['rpm_2'] = 'brpm'
UNIT['brv_2'] = 's'
UNIT['tachypnea_1'] = 'brpm'
UNIT['bradypnea_1'] = 'brpm'
UNIT['tachypnea_2'] = 'brpm'
UNIT['bradypnea_2'] = 'brpm'
UNIT['bior_1'] = ''
UNIT['bior_2'] = ''
UNIT['temp'] = '°C'
UNIT['n_steps'] = ''
UNIT['stress'] = ''
UNIT['sleep'] = '%'
UNIT['spo2'] = ''
UNIT['pulseox'] = ''
UNIT['bodybattery'] = '%'


STANDARD = {}
STANDARD['bpm'] = '[60 - 100] Resting'
STANDARD['sdnn'] = '> 100 Resting'
STANDARD['hrv'] = '> 100 Resting'
STANDARD['tachycardia'] = ''
STANDARD['bradycardia'] = ''
STANDARD['qt'] = ''
STANDARD['rpm_1'] = '[6 - 20] Resting'
STANDARD['brv_1'] = ''
STANDARD['rpm_2'] = '[6 - 20] Resting'
STANDARD['brv_2'] = ''
STANDARD['tachypnea_1'] = ''
STANDARD['bradypnea_1'] = ''
STANDARD['tachypnea_2'] = ''
STANDARD['bradypnea_2'] = ''
STANDARD['bior_1'] = ''
STANDARD['bior_2'] = ''
STANDARD['temp'] = ''
STANDARD['n_steps'] = ''
STANDARD['stress'] = ''
STANDARD['sleep'] = ''
STANDARD['spo2'] = ''
STANDARD['bodybattery'] = ''

VALUE_TYPE = {}
VALUE_TYPE['bpm'] = 'Median'
VALUE_TYPE['sdnn'] = 'Median'
VALUE_TYPE['hrv'] = 'Median'
VALUE_TYPE['tachycardia'] = 'Median'
VALUE_TYPE['bradycardia'] = 'Median'
VALUE_TYPE['qt'] = 'Median'
VALUE_TYPE['rpm_1'] = 'Median'
VALUE_TYPE['brv_1'] = 'Median'
VALUE_TYPE['rpm_2'] = 'Median'
VALUE_TYPE['brv_2'] = 'Median'
VALUE_TYPE['bior_1'] = 'Median'
VALUE_TYPE['bior_2'] = 'Median'
VALUE_TYPE['tachypnea_1'] = 'Median'
VALUE_TYPE['bradypnea_1'] = 'Median'
VALUE_TYPE['tachypnea_2'] = 'Median'
VALUE_TYPE['bradypnea_2'] = 'Median'
VALUE_TYPE['temp'] = 'Median'
VALUE_TYPE['n_steps'] = ''
VALUE_TYPE['stress'] = ''
VALUE_TYPE['sleep'] = ''
VALUE_TYPE['spo2'] = ''
VALUE_TYPE['pulseox'] = ''
VALUE_TYPE['bodybattery'] = ''

RANGE = {}
RANGE['bpm'] = [40, 140]
RANGE['sdnn'] = [0, 1000]
RANGE['hrv'] = [0, 1000]
RANGE['tachycardia'] = []
RANGE['bradycardia'] = []
RANGE['qt'] = [350, 750]
RANGE['rpm_1'] = [5, 35]
RANGE['brv_1'] = [0, 4]
RANGE['rpm_2'] = [5, 35]
RANGE['brv_2'] = [0, 4]
RANGE['tachypnea_1'] = []
RANGE['bradypnea_1'] = []
RANGE['tachypnea_2'] = []
RANGE['bradypnea_2'] = []
RANGE['bior_1'] = [0, 2]
RANGE['bior_2'] = [0, 2]
RANGE['temp'] = [20, 40]
RANGE['n_steps'] = [0, 200]
RANGE['stress'] = []
RANGE['sleep'] = []
RANGE['spo2'] = []
RANGE['pulseox'] = []
RANGE['bodybattery'] = []


DEFINITION = {}
DEFINITION['bpm'] = "Number of Heart Beat Per Minute"
DEFINITION['sdnn'] = "Standard deviation of times between successive QRS complexes (RR intervals)"
DEFINITION['hrv'] = "Standard deviation of times between successive QRS complexes (RR intervals)"
DEFINITION['tachycardia'] = "Number of Heart Beat higher than 100 bpm at rest"
DEFINITION['bradycardia'] = "Number of Heart Beat lower than 50 bpm at rest"
DEFINITION['qt'] = "Time between Q and T waves in millisecond normalized by Framingham formula"
DEFINITION['rpm_1'] = "Number of Respiratory Cycle Per Minute"
DEFINITION['brv_1'] = "Standard deviation of durations between successive respiratory cycles"
DEFINITION['rpm_2'] = "Number of Respiratory Cycle Per Minute"
DEFINITION['brv_2'] = "Standard deviation of durations between successive respiratory cycles"
DEFINITION['tachypnea_1'] = "Number of Respiratory Cycle higher than 20 cpm at rest"
DEFINITION['bradypnea_1'] = "Number of Respiratory Cycle lower than 6 cpm at rest"
DEFINITION['tachypnea_2'] = "Number of Respiratory Cycle higher than 20 cpm at rest"
DEFINITION['bradypnea_2'] = "Number of Respiratory Cycle lower than 6 cpm at rest"
DEFINITION['bior_1'] = "Ratio of inhalation time to exhalation time"
DEFINITION['bior_2'] = "Ratio of inhalation time to exhalation time" 
DEFINITION['temp'] = ''
DEFINITION['n_steps'] = ''
DEFINITION['stress'] = ''
DEFINITION['sleep'] = ''
DEFINITION['spo2'] = ''
DEFINITION['pulseox'] = ''
DEFINITION['bodybattery'] = ''

IMAGE = {}
CARDIO = "cardiology.png"
RESPI = "respiratory.png"
IMAGE['bpm'] = CARDIO
IMAGE['sdnn'] = CARDIO
IMAGE['hrv'] = CARDIO
IMAGE['tachycardia'] = CARDIO
IMAGE['bradycardia'] = CARDIO
IMAGE['qt'] = CARDIO
IMAGE['rpm_1'] = RESPI
IMAGE['brv_1'] = RESPI
IMAGE['rpm_2'] = RESPI
IMAGE['brv_2'] = RESPI
IMAGE['tachypnea_1'] = RESPI
IMAGE['bradypnea_1'] = RESPI
IMAGE['tachypnea_2'] = RESPI
IMAGE['bradypnea_2'] = RESPI
IMAGE['bior_1'] = RESPI
IMAGE['bior_2'] = RESPI
IMAGE['temp'] = "temperature.png"
IMAGE['n_steps'] = "steps.png"
IMAGE['stress'] = "stress.png"
IMAGE['sleep'] = "sleep.png"
IMAGE['spo2'] = "pulseox.png"
IMAGE['pulseox'] = "pulseox.png"
IMAGE['bodybattery'] = "calories.png"


MONTHS = {}
MONTHS['January'] = "01"
MONTHS["1"] = "January"
MONTHS['February'] = "02"
MONTHS["2"] = "February"
MONTHS['March'] = "03"
MONTHS["3"] = "March"
MONTHS['April'] = "04"
MONTHS["4"] = "April"
MONTHS['May'] = "05"
MONTHS["5"] = "May"
MONTHS['June'] = "06"
MONTHS["6"] = "June"
MONTHS['July'] = "07"
MONTHS["7"] = "July"
MONTHS['August'] = "08"
MONTHS["8"] = "August"
MONTHS['September'] = "09"
MONTHS["9"] = "September"
MONTHS['October'] = "10"
MONTHS["10"] = "October"
MONTHS['November'] = "11"
MONTHS["11"] = "November"
MONTHS['December'] = "12"
MONTHS["12"] = "December"