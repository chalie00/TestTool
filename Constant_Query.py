
# =====================================================   Uncooled Query =====================================================
# (2024.07.12) Uncooled Type Query Data Store
uncooled_normal_q = {'normal': ''}
uncooled_zoom_q = {'zoom': '', 'magnification': ''}
uncooled_focus_q = {'focus': ''}
uncooled_comm_q = {'mode': '', 'add': '', 'baud': '', 'word': '',
                   'stop': '', 'parity': '', 'protocol': ''}
uncooled_lens_q = {'af_trigger': '', 'zoom_spd': '', 'focus_spd': '', 'af_mode': '',
                   'af_interval': '', 'fov_position': '', 'query_mode': ''}
uncooled_image_q = {'dis': '', 'dnr': '', 'flip': '', 'mirror': '',
                    'freeze': '', 'dzoom': '', 'dzoom_position': ''}
uncooled_sensor_q = {'histogram': '', 'brightness': '', 'contrast': '', 'white_hot': '',
                     'pseudo': '', 'edge': ''}
uncooled_cali_q = {'trigger': '', 'mode': '', 'interval': ''}
uncooled_etc_q = {'save': '', 'cvbs': '', 'display': ''}
uncooled_status_q = {'boot': '', 'board_t': '', 'lens_t': '', 'sensor_t': '',
                     'fan': '', 'telemetry': '', 'calibration': '', 'af': ''}
uncooled_version_q = {'sensor': '', 'lens': '', 'main': '', 'main_y': '',
                      'main_m_d': '', 'osd': '', 'osd_y': '', 'osd_m_d': ''}
uncooled_encoder_q = {'zoom_max': '', 'zoom_min': '', 'focus_max': '', 'focus_min': ''}

# (2024.07.16) Uncooled Type Query MSB+LSB Data Store
# position, speed, mode
zoom_msb_lsb = [uncooled_zoom_q['zoom'], uncooled_lens_q['zoom_spd'], uncooled_image_q['dzoom'],
                uncooled_image_q['dzoom_position']]
focus_msb_lsb = [uncooled_focus_q['focus'], uncooled_lens_q['focus_spd'], uncooled_lens_q['af_mode']
                 ]
fov_msb_lsb = [uncooled_lens_q['fov_position']]

# =====================================================   NYX Query =====================================================
# (2024.07.24): NYX Series Query Data Store
# zoom_pos, focus_pos, fov, zoom_spd, focus_spd, dzoom
# lens_pos_q = ['NYX.GET#lens_zpos', 'NYX.GET#lens_fpos', 'NYX.GET#lens_cfov',
#               'NYX.GET#lens_zspd', 'NYX.GET#lens_fspd', 'NYX.GET#isp0_dzen']
cooled_lens_pos_spd = [0, 0, 0, 0, 0, 0, 0]