# (2024.08.14): Added for DRS Response
import Constant as Cons


# Bit0:Mirror, Bit1:Flip, Bit2:Invert, Bit8~Bit11:Digital Zoom, Bit12~Bit15:Color Palette
def check_data01(data):
    dzoom = ['x1', 'x2', 'x4', 'x8']
    color_pallet = ['GRAY', 'RAINBOW', 'IRON', 'JET', 'THERMAL', 'BLUE ORANGe CB',
                    'SMART', 'COOL', 'GRAY+RAINBOW', 'GRAY+JET', 'GRAY+IRON']

    Cons.drs_response.update({
        'mirror': 'ON' if data[15] == '1' else 'OFF',
        'flip': 'ON' if data[14] == '1' else 'OFF',
        'invert': 'ON' if data[13] == '1' else 'OFF',
        'dzoom': dzoom[max(0, int(data[4:8], 2) - 1)],
        'color': color_pallet[int(data[0:4], 2)]
    })


# Bit4~Bit7:Gamma Filter, Bit8~Bit11:AGC Mode
def check_data02(data):
    gamma = ['0.7', '0.8', '0.9', '1.0', '1.1', '1.2', '1.3', '1.4']
    agc_mode = ['MGC', 'Low', 'Middle', 'High']

    Cons.drs_response.update({
        'gamma': gamma[int(data[8:12], 2)],
        'agc_mode': agc_mode[int(data[4:8], 2)]
    })


# Data3 is ROIx Start Position x Data4 is Roix Start Position y
# Data7 is Contrast, Data8 is Brightness
def convert_to_deci(data):
    deci_data = int(data, 2)
    return deci_data


# Bit0~Bit7:IDE Level, Bit8~Bit15:AGC Adapt Frame Number
def check_data05(data):
    Cons.drs_response.update({
        'ide': int(data[8:16], 2),
        'agc_frame': int(data[0:8], 2)
    })


# Bit0~Bit3:Calibration Mode, Bit4~Bit15:Calibration Interval Time
def check_data06(data):
    cali_mode_title = ['Manual', 'Auto', 'Interval']

    Cons.drs_response.update({
        'cal_mode': cali_mode_title[int(data[12:16], 2)],
        'cal_interval_time': int(data[0:12], 2)
    })


# F/W Version Information(Bit0~Bit7:Minor Number, Bit8~Bit15:Major Number)
def check_data09(data):
    minor_fw = int(data[8:16], 2)
    major_fw = int(data[0:8], 2)
    fw = str(format(major_fw, 'x')) + str(format(minor_fw, 'x'))
    Cons.drs_response['fw'] = fw


# Bit0:Temp Infor Enable, Bit1:Colorbar Enable, Bit2:Center Mark Enable, Bit3:Min/Max Mark Enable
def check_data14(data):
    bit_mapping = {
        15: 'temp_info',
        14: 'colorbar',
        13: 'center_mark',
        12: 'min_max'
    }

    Cons.drs_response.update({
        name: 'ON' if data[bit] == '1' else 'OFF'
        for bit, name in bit_mapping.items()
    })


# Bit0~Bit7:Focal Length, Bit8~Bit9:TBD, Bit10:Zoom Move Flag, Bit11:A/F Flag
def check_data17(data):
    Cons.drs_response.update({
        'focal_len': int(data[8:16], 2),
        'TBD': int(data[6:10]),
        'zoom_move_flag': int(data[5], 2),
        'af_flag': int(data[4], 2)
    })


# Bit0~Bit7:Frame Rate Value Bit8~Bit15:DataTx Mode Value
def check_data18(data):
    Cons.drs_response.update({
        'frame_rate': int(data[8:16], 2),
        'tx_mode': int(data[0:8], 2)
    })


# Bit0:ROI0 Enable, Bit1:ROI1 Enable,… Bit9:ROI9 Enable, Bit10:Min/Max Enable,
# Bit11:Mask0 Enable, Bit12:Mask1 Enable, Bit13:Mask2 Enable
def check_data46(data):
    Cons.drs_response.update({
        'roi0': int(data[15], 2),
        'roi1': int(data[14], 2),
        'roi2': int(data[13], 2),
        'roi3': int(data[12], 2),
        'roi4': int(data[11], 2),
        'roi5': int(data[10], 2),
        'roi6': int(data[9], 2),
        'roi7': int(data[8], 2),
        'roi8': int(data[7], 2),
        'roi9': int(data[6], 2),
        'min_max_en': int(data[5], 2),
        'mask0': int(data[5], 2),
        'mask1': int(data[4], 2),
        'mask2': int(data[3], 2)
    })


# Bit0:ROI0 Alarm, Bit1:ROI1 Alarm,… Bit9:ROI9 Alarm
def check_data47(data):
    Cons.drs_response.update({
        'arm0': int(data[15], 2),
        'arm1': int(data[14], 2),
        'arm2': int(data[13], 2),
        'arm3': int(data[12], 2),
        'arm4': int(data[11], 2),
        'arm5': int(data[10], 2),
        'arm6': int(data[9], 2),
        'arm7': int(data[8], 2),
        'arm8': int(data[7], 2),
        'arm9': int(data[6], 2)
    })