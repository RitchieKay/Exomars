#!/usr/bin/python
import sys
import re
import os.path

def main():

    if len(sys.argv) < 2:
        print 'Usage:', sys.argv[0], '<file name>'
        sys.exit(-1)

    a = ActionSequenceProcessor()

    if os.path.isdir(sys.argv[1]):
        a.source_code(sys.argv[1])
    else:
        a.s2k_obsm(sys.argv[1])

class ActionSequenceProcessor:

    def __init__(self):
        self.acseq_ids = {}
        for i in range(500):  
            self.acseq_ids[i] = 'UNKNOWN'

            self.acseq_ids[252]	 = 'ACSEQ_AIT_SA_DEPLOYMENT'
            self.acseq_ids[230]	= 'ACSEQ_APM_TO_CRUISE'
            self.acseq_ids[237]	= 'ACSEQ_COMMON_L2_L3_LAST_ACTIONS'
            self.acseq_ids[238]	= 'ACSEQ_CONFIGURE_TM_PMON_TEMPORARY_OUT_LIMIT' 
            self.acseq_ids[218]	= 'ACSEQ_CONNECT_TGO_BATTERY'
            self.acseq_ids[260]	= 'ACSEQ_DELETE_EDM_SEP_RTPU_CTPU_SSID_FROM_MTL'
            self.acseq_ids[125]	= 'ACSEQ_DISABLE_AEROBRAKING_FDIR'
            self.acseq_ids[97]	= 'ACSEQ_DISABLE_ALL_EDM_FDIR'
            self.acseq_ids[153]	= 'ACSEQ_DISABLE_ALL_RW_L1_FDIR'
            self.acseq_ids[157]	= 'ACSEQ_DISABLE_RW_1_L2_FDIR'
            self.acseq_ids[158]	= 'ACSEQ_DISABLE_RW_2_L2_FDIR'
            self.acseq_ids[159]	= 'ACSEQ_DISABLE_RW_3_L2_FDIR'
            self.acseq_ids[160]	= 'ACSEQ_DISABLE_RW_4_L2_FDIR'
            self.acseq_ids[258]	= 'ACSEQ_DISABLE_TGO_EDM_CHECKOUT_FDIR'
            self.acseq_ids[248]	= 'ACSEQ_EDM_APP_TO_SAFE_AND_FDIR_FOR_EDM_SAFE'
            self.acseq_ids[68]	= 'ACSEQ_EDM_CHK_TO_PRESEP'
            self.acseq_ids[67]	= 'ACSEQ_EDM_CHK_TO_SERV'
            self.acseq_ids[138]	= 'ACSEQ_EDM_DISABLE_THERMAL_CONTROL'
            self.acseq_ids[98]	= 'ACSEQ_EDM_OPEN_BATTERY_RELAY_CORE'
            self.acseq_ids[251]	= 'ACSEQ_EDM_OPEN_RTPU_HG'
            self.acseq_ids[77]	= 'ACSEQ_EDM_SAFE_TO_SERV'
            self.acseq_ids[141]	= 'ACSEQ_EDM_SAFE_TO_SERV_CORE_PART_1'
            self.acseq_ids[142]	= 'ACSEQ_EDM_SAFE_TO_SERV_CORE_PART_2'
            self.acseq_ids[122]	= 'ACSEQ_EDM_SEPARATION'
            self.acseq_ids[66]	= 'ACSEQ_EDM_SERV_TO_CHK'
            self.acseq_ids[71]	= 'ACSEQ_EDM_SETUP_FOR_SEPARATION'
            self.acseq_ids[65]	= 'ACSEQ_EDM_STARTUP'
            self.acseq_ids[70]	= 'ACSEQ_EDM_TCS_DISABLE'
            self.acseq_ids[64]	= 'ACSEQ_EDM_TO_OFF'
            self.acseq_ids[79]	= 'ACSEQ_EDM_TO_SAFE'
            self.acseq_ids[123]	= 'ACSEQ_EDM_TO_SAFE_CORE'
            self.acseq_ids[78]	= 'ACSEQ_EDM_TO_SAFE_THEN_TO_SERV'
            self.acseq_ids[37]	= 'ACSEQ_ENABLE_1553_SMU_FDIR'
            self.acseq_ids[124]	= 'ACSEQ_ENABLE_AEROBRAKING_FDIR'
            self.acseq_ids[187]	= 'ACSEQ_ENABLE_ALL_RW_FDIR'
            self.acseq_ids[126]	= 'ACSEQ_ENABLE_CU_MIMU_L1_FDIR_NO_ACC'
            self.acseq_ids[36]	= 'ACSEQ_ENABLE_CU_PCDU_L1_FDIR'
            self.acseq_ids[35]	= 'ACSEQ_ENABLE_CU_PCU_L1_FDIR'
            self.acseq_ids[130]	= 'ACSEQ_ENABLE_CU_XDSTTX_AND_TWTA_FDIR'
            self.acseq_ids[186]	= 'ACSEQ_ENABLE_FCG_FDIR'
            self.acseq_ids[149]	= 'ACSEQ_ENABLE_PCDU_RCS_FDIR'
            self.acseq_ids[150]	= 'ACSEQ_ENABLE_PCU_L2_APS_VOLT_FDIR_IN_V4'
            self.acseq_ids[223]	= 'ACSEQ_ENABLE_PL_1553_BUS_MONITORING'
            self.acseq_ids[250]	= 'ACSEQ_ENABLE_RW_TORQUE_FDIR'
            self.acseq_ids[143]	= 'ACSEQ_ENABLE_STR_L1_AAD_TRANSITION_FDIR'
            self.acseq_ids[162]	= 'ACSEQ_ENABLE_STR_L1_FDIR'
            self.acseq_ids[129]	= 'ACSEQ_ENABLE_SURVIVAL_LINES_MONITORING'
            self.acseq_ids[31]	= 'ACSEQ_ENABLE_TCS_L1_FDIR_PART1'
            self.acseq_ids[32]	= 'ACSEQ_ENABLE_TCS_L1_FDIR_PART2'
            self.acseq_ids[33]	= 'ACSEQ_ENABLE_TCS_SLOTS_PART1'
            self.acseq_ids[34]	= 'ACSEQ_ENABLE_TCS_SLOTS_PART2'
            self.acseq_ids[42]	= 'ACSEQ_ENABLE_TCS_SLOTS_PART3'
            self.acseq_ids[240]	= 'ACSEQ_ENABLE_TCS_SLOTS_PART4'
            self.acseq_ids[259]	= 'ACSEQ_ENABLE_TGO_EDM_SERV_FDIR_FROM_CHECKOUT'
            self.acseq_ids[220]	= 'ACSEQ_ENTER_INIT_ENABLE_FDIR_SERVICE_AND_ACSEQ_FOR_FIRST_SAM'
            self.acseq_ids[144]	= 'ACSEQ_ENTER_INIT_PREPARATION'
            self.acseq_ids[145]	= 'ACSEQ_ENTER_INIT_PROP_VENTING'
            self.acseq_ids[147]	= 'ACSEQ_ENTER_INIT_SA_DEPLOYMENT_WITH_DMD_2'
            self.acseq_ids[148]	= 'ACSEQ_ENTER_INIT_SWITCH_ON_AND_CONFIGURE_RF'
            self.acseq_ids[247]	= 'ACSEQ_ENTER_LAUNCH_INIT_COMMON_PART_1'
            self.acseq_ids[117]	= 'ACSEQ_ENTER_RECONF_INIT'
            self.acseq_ids[30]	= 'ACSEQ_ENTER_RECONF_LAUNCH'
            self.acseq_ids[119]	= 'ACSEQ_ENTER_SAFE_1'
            self.acseq_ids[229]	= 'ACSEQ_ENTER_SAFE_1_CONFIGURE_SPECIFIC_FDIR'
            self.acseq_ids[121]	= 'ACSEQ_ENTER_SAFE_2'
            self.acseq_ids[228]	= 'ACSEQ_ENTER_SAFE_2_CONFIGURE_SPECIFIC_FDIR'
            self.acseq_ids[120]	= 'ACSEQ_ENTER_SAFE_A'
            self.acseq_ids[233]	= 'ACSEQ_ENTER_SAFE_COMMON_PART_1'
            self.acseq_ids[244]	= 'ACSEQ_ENTER_SAFE_COMMON_PART_2'
            self.acseq_ids[245]	= 'ACSEQ_ENTER_SAFE_CONFIGURE_COMMON_FDIR'
            self.acseq_ids[243]	= 'ACSEQ_ENTER_SAFE_INIT_COMMON_PART'
            self.acseq_ids[242]	= 'ACSEQ_ENTER_SAFE_PREPARE_AND_ENTER_SAM'
            self.acseq_ids[191]	= 'ACSEQ_ENTER_SAFE_SWITCH_ON_AND_CONFIGURE_RF'
            self.acseq_ids[47]	= 'ACSEQ_ENTER_TEST'
            self.acseq_ids[226]	= 'ACSEQ_EXIT_FAIL_OP'
            self.acseq_ids[128]	= 'ACSEQ_GNC_MANUAL_THRUST_CONFIGURATION_FOR_VENTING'
            self.acseq_ids[168]	= 'ACSEQ_GNC_MODE_REINIT_AEBM'
            self.acseq_ids[169]	= 'ACSEQ_GNC_MODE_REINIT_NOMP'
            self.acseq_ids[170]	= 'ACSEQ_GNC_MODE_REINIT_NOMR'
            self.acseq_ids[171]	= 'ACSEQ_GNC_MODE_REINIT_OCM'
            self.acseq_ids[172]	= 'ACSEQ_GNC_MODE_REINIT_SAM'
            self.acseq_ids[173]	= 'ACSEQ_GNC_MODE_REINIT_SBM'
            self.acseq_ids[174]	= 'ACSEQ_GNC_MODE_TRANSITION_AEBM_TO_NOMP'
            self.acseq_ids[175]	= 'ACSEQ_GNC_MODE_TRANSITION_AEBM_TO_NOMR'
            self.acseq_ids[176]	= 'ACSEQ_GNC_MODE_TRANSITION_NOMP_TO_AEBM'
            self.acseq_ids[177]	= 'ACSEQ_GNC_MODE_TRANSITION_NOMP_TO_NOMR'
            self.acseq_ids[178]	= 'ACSEQ_GNC_MODE_TRANSITION_NOMP_TO_OCM'
            self.acseq_ids[179]	= 'ACSEQ_GNC_MODE_TRANSITION_NOMR_TO_AEBM'
            self.acseq_ids[180]	= 'ACSEQ_GNC_MODE_TRANSITION_NOMR_TO_NOMP'
            self.acseq_ids[181]	= 'ACSEQ_GNC_MODE_TRANSITION_NOMR_TO_OCM'
            self.acseq_ids[182]	= 'ACSEQ_GNC_MODE_TRANSITION_OCM_TO_NOMP'
            self.acseq_ids[183]	= 'ACSEQ_GNC_MODE_TRANSITION_OCM_TO_NOMR'
            self.acseq_ids[184]	= 'ACSEQ_GNC_MODE_TRANSITION_OCM_TO_SAM'
            self.acseq_ids[185]	= 'ACSEQ_GNC_MODE_TRANSITION_SAM_TO_NOMP'
            self.acseq_ids[188]	= 'ACSEQ_GNC_MODE_TRANSITION_SBM_TO_SAM'
            self.acseq_ids[165]	= 'ACSEQ_GNC_NOMP_SAFE_1'
            self.acseq_ids[166]	= 'ACSEQ_GNC_NOMP_SAFE_A'
            self.acseq_ids[167]	= 'ACSEQ_GNC_NOMR_SAFE_1'
            self.acseq_ids[194]	= 'ACSEQ_GNC_SUBMODE_REINIT_NOMP_AK'
            self.acseq_ids[195]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_AEBM_PASS_TO_RD'
            self.acseq_ids[196]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_NOMP_AK_TO_ARD'
            self.acseq_ids[197]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_NOMP_AK_TO_EDMS'
            self.acseq_ids[198]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_NOMP_AK_TO_SLEW'
            self.acseq_ids[199]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_NOMP_ARD_TO_SLEW'
            self.acseq_ids[201]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_NOMP_SLEW_TO_AK'
            self.acseq_ids[202]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_NOMP_SLEW_TO_ARD'
            self.acseq_ids[203]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_NOMR_CRUISE_TO_UNLOADING'
            self.acseq_ids[204]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_NOMR_UNLOADING_TO_CRUISE'
            self.acseq_ids[205]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_OCM_AK_TO_ME_BOOST'
            self.acseq_ids[206]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_OCM_AK_TO_RCT_BOOST'
            self.acseq_ids[207]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_OCM_ME_BOOST_TO_AK'
            self.acseq_ids[208]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_OCM_RCT_BOOST_TO_AK'
            self.acseq_ids[209]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_OCM_RCT_BOOST_TO_ME_BOOST'
            self.acseq_ids[210]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_SAM_ARD_TO_RD'
            self.acseq_ids[211]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_SAM_ARD_TO_SP'
            self.acseq_ids[212]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_SAM_RD_TO_ROTATION'
            self.acseq_ids[213]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_SAM_ROTATION_TO_ARD'
            self.acseq_ids[214]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_SAM_ROTATION_TO_SP'
            self.acseq_ids[217]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_SAM_SPIN_TO_ARD'
            self.acseq_ids[215]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_SAM_SP_TO_ARD'
            self.acseq_ids[216]	= 'ACSEQ_GNC_SUBMODE_TRANSITION_SAM_SP_TO_SPIN'
            self.acseq_ids[132]	= 'ACSEQ_HGA_HRM_RELEASE'
            self.acseq_ids[86]	= 'ACSEQ_L1_ACS_1_AND_2_SWITCH_OFF'
            self.acseq_ids[253]	= 'ACSEQ_L1_AEROBRAKING_ORBIT_PERIOD_RECOVERY'
            self.acseq_ids[62]	= 'ACSEQ_L1_AEROBRAKING_RECOVERY'
            self.acseq_ids[89]	= 'ACSEQ_L1_CASSIS_SWITCH_OFF'
            self.acseq_ids[54]	= 'ACSEQ_L1_CSS_RECOVERY'
            self.acseq_ids[72]	= 'ACSEQ_L1_EDM_CTPU_POWER_CYCLE'
            self.acseq_ids[74]	= 'ACSEQ_L1_EDM_OPEN_BATTERY_SWITCHES'
            self.acseq_ids[90]	= 'ACSEQ_L1_EDM_OVERTEMP'
            self.acseq_ids[81]	= 'ACSEQ_L1_EDM_POWER_CONSUMTION_RECOVERY'
            self.acseq_ids[73]	= 'ACSEQ_L1_EDM_RTPU_POWER_CYCLE'
            self.acseq_ids[80]	= 'ACSEQ_L1_EDM_SEP_ABORT'
            self.acseq_ids[76]	= 'ACSEQ_L1_EDM_TO_SAFE_CTPU_OVERTEMP'
            self.acseq_ids[75]	= 'ACSEQ_L1_EDM_TO_SAFE_RTPU_OVERTEMP'
            self.acseq_ids[84]	= 'ACSEQ_L1_EUT_SWITCH_OFF'
            self.acseq_ids[50]	= 'ACSEQ_L1_FCG2_OFF_CSS_RW_RECOVERY'
            self.acseq_ids[51]	= 'ACSEQ_L1_FCG3_OFF_CSS_RW_RECOVERY'
            self.acseq_ids[52]	= 'ACSEQ_L1_FCG5_OFF_CSS_RW_RECOVERY'
            self.acseq_ids[53]	= 'ACSEQ_L1_FCG6_OFF_CSS_RW_RECOVERY'
            self.acseq_ids[88]	= 'ACSEQ_L1_FREND_SWITCH_OFF'
            self.acseq_ids[56]	= 'ACSEQ_L1_IMU_RECOVERY'
            self.acseq_ids[134]	= 'ACSEQ_L1_MIMU_RECOVERY_FAIL_OP'
            self.acseq_ids[133]	= 'ACSEQ_L1_MIMU_RECOVERY_FAIL_SAFE'
            self.acseq_ids[85]	= 'ACSEQ_L1_NOMAD_SWITCH_OFF'
            self.acseq_ids[5]	= 'ACSEQ_L1_PCDU_CORE_RECOVERY'
            self.acseq_ids[61]	= 'ACSEQ_L1_PCDU_RCS_RECOVERY'
            self.acseq_ids[116]	= 'ACSEQ_L1_PCDU_RCS_RECOVERY_FAIL_OP'
            self.acseq_ids[114]	= 'ACSEQ_L1_PCDU_RCS_RECOVERY_FAIL_SAFE'
            self.acseq_ids[4]	= 'ACSEQ_L1_PCU_RECOVERY'
            self.acseq_ids[83]	= 'ACSEQ_L1_PDHU_CU_SWITCH_OFF'
            self.acseq_ids[27]	= 'ACSEQ_L1_PF1553_BUS_LINE_RECOVERY'
            self.acseq_ids[96]	= 'ACSEQ_L1_PL1553_BUS_LINE_RECOVERY'
            self.acseq_ids[63]	= 'ACSEQ_L1_RF_CHAIN_RECOVERY'
            self.acseq_ids[57]	= 'ACSEQ_L1_RW1_FAILED'
            self.acseq_ids[58]	= 'ACSEQ_L1_RW2_FAILED'
            self.acseq_ids[59]	= 'ACSEQ_L1_RW3_FAILED'
            self.acseq_ids[60]	= 'ACSEQ_L1_RW4_FAILED'
            self.acseq_ids[82]	= 'ACSEQ_L1_SET_PDHU_CU_RT_FAILED'
            self.acseq_ids[3]	= 'ACSEQ_L1_SMU_IO_RECOVERY'
            self.acseq_ids[46]	= 'ACSEQ_L1_SMU_IO_RECOVERY_FAIL_OP'
            self.acseq_ids[44]	= 'ACSEQ_L1_SMU_IO_RECOVERY_FAIL_SAFE'
            self.acseq_ids[55]	= 'ACSEQ_L1_STR_RECOVERY'
            self.acseq_ids[136]	= 'ACSEQ_L1_STR_RECOVERY_FAIL_OP'
            self.acseq_ids[135]	= 'ACSEQ_L1_STR_RECOVERY_FAIL_SAFE'
            self.acseq_ids[87]	= 'ACSEQ_L1_STR_TRANSITION_TO_AAD'
            self.acseq_ids[6]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG1'
            self.acseq_ids[15]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG10'
            self.acseq_ids[16]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG11'
            self.acseq_ids[17]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG12'
            self.acseq_ids[18]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG13'
            self.acseq_ids[19]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG14'
            self.acseq_ids[20]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG15'
            self.acseq_ids[21]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG16'
            self.acseq_ids[22]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG17'
            self.acseq_ids[23]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG18'
            self.acseq_ids[24]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG19'
            self.acseq_ids[7]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG2'
            self.acseq_ids[25]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG20'
            self.acseq_ids[26]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG21'
            self.acseq_ids[8]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG3'
            self.acseq_ids[9]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG4'
            self.acseq_ids[10]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG5'
            self.acseq_ids[11]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG6'
            self.acseq_ids[12]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG7'
            self.acseq_ids[13]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG8'
            self.acseq_ids[14]	= 'ACSEQ_L1_TCS_HEATER_RECOVERY_HG9'
            self.acseq_ids[1]	= 'ACSEQ_L2_RECOVERY'
            self.acseq_ids[91]	= 'ACSEQ_L2_RW1_FAILED' 
            self.acseq_ids[92]	= 'ACSEQ_L2_RW2_FAILED'
            self.acseq_ids[93]	= 'ACSEQ_L2_RW3_FAILED'
            self.acseq_ids[94]	= 'ACSEQ_L2_RW4_FAILED'
            self.acseq_ids[2]	= 'ACSEQ_L3_RECOVERY'
            self.acseq_ids[263]	= 'ACSEQ_LAUNCH_TO_INIT_CONFIGURE_FDIR'
            self.acseq_ids[28]	= 'ACSEQ_PCDU_SWITCH_OFF_HEATER_GROUPS_PART_1'
            self.acseq_ids[234]	= 'ACSEQ_PCDU_SWITCH_OFF_HEATER_GROUPS_PART_2'
            self.acseq_ids[29]	= 'ACSEQ_PCDU_SWITCH_ON_HEATER_GROUPS_PART_1'
            self.acseq_ids[235]	= 'ACSEQ_PCDU_SWITCH_ON_HEATER_GROUPS_PART_2'
            self.acseq_ids[189]	= 'ACSEQ_POWER_ON_RW'
            self.acseq_ids[225]	= 'ACSEQ_PREPARE_FAIL_OP'
            self.acseq_ids[131]	= 'ACSEQ_PROP_PRIMING_IN_INIT'
            self.acseq_ids[127]	= 'ACSEQ_PROP_VENTING_VALVES_OPENING'
            self.acseq_ids[154]	= 'ACSEQ_RECONFIGURE_SMU_IO_CORE'
            self.acseq_ids[236]	= 'ACSEQ_RECONF_LAUNCH_CONFIGURE_FDIR'
            self.acseq_ids[140]	= 'ACSEQ_SA_DEPLOYMENT_RELEASE_WING_MZ_HRM'
            self.acseq_ids[139]	= 'ACSEQ_SA_DEPLOYMENT_RELEASE_WING_PZ_HRM'
            self.acseq_ids[101]	= 'ACSEQ_SC_MODE_TRANSITION_INIT_TO_ROUT'
            self.acseq_ids[118]	= 'ACSEQ_SC_MODE_TRANSITION_LAUNCH_TO_INIT_PART_1'
            self.acseq_ids[115]	= 'ACSEQ_SC_MODE_TRANSITION_LAUNCH_TO_INIT_PART_2'
            self.acseq_ids[100]	= 'ACSEQ_SC_MODE_TRANSITION_LAUNCH_TO_TEST'
            self.acseq_ids[107]	= 'ACSEQ_SC_MODE_TRANSITION_MAN_A_TO_ROUT'
            self.acseq_ids[103]	= 'ACSEQ_SC_MODE_TRANSITION_MAN_C_TO_ROUT'
            self.acseq_ids[105]	= 'ACSEQ_SC_MODE_TRANSITION_MAN_R_TO_ROUT'
            self.acseq_ids[106]	= 'ACSEQ_SC_MODE_TRANSITION_ROUT_TO_MAN_A'
            self.acseq_ids[102]	= 'ACSEQ_SC_MODE_TRANSITION_ROUT_TO_MAN_C'
            self.acseq_ids[104]	= 'ACSEQ_SC_MODE_TRANSITION_ROUT_TO_MAN_R'
            self.acseq_ids[108]	= 'ACSEQ_SC_MODE_TRANSITION_ROUT_TO_SCR'
            self.acseq_ids[110]	= 'ACSEQ_SC_MODE_TRANSITION_SAFE_1_TO_ROUT'
            self.acseq_ids[112]	= 'ACSEQ_SC_MODE_TRANSITION_SAFE_2_TO_SAFE_1'
            self.acseq_ids[113]	= 'ACSEQ_SC_MODE_TRANSITION_SAFE_2_TO_SAFE_A'
            self.acseq_ids[111]	= 'ACSEQ_SC_MODE_TRANSITION_SAFE_A_TO_ROUT'
            self.acseq_ids[109]	= 'ACSEQ_SC_MODE_TRANSITION_SCR_TO_ROUT'
            self.acseq_ids[99]	= 'ACSEQ_SC_MODE_TRANSITION_TEST_TO_LAUNCH'
            self.acseq_ids[231]	= 'ACSEQ_SELECT_NOMR_AUTO_TM_MODE'
            self.acseq_ids[232]	= 'ACSEQ_SELECT_NOMR_GROUND_TM_MODE'
            self.acseq_ids[254]	= 'ACSEQ_SET_ALL_EDM_HG_OFF_IN_SAT_CONF'
            self.acseq_ids[246]	= 'ACSEQ_SET_TM_MODE_1'
            self.acseq_ids[239]	= 'ACSEQ_START_TGO_TCS'
            self.acseq_ids[249]	= 'ACSEQ_SWAP_PCDU_AND_1553_PF_LINE'
            self.acseq_ids[48]	= 'ACSEQ_SWITCH_OFF_ACS'
            self.acseq_ids[222]	= 'ACSEQ_SWITCH_OFF_ALL_CU_RCT'
            self.acseq_ids[137]	= 'ACSEQ_SWITCH_OFF_ALL_CU_RCT_WITH_FLUSH'
            self.acseq_ids[95]	= 'ACSEQ_SWITCH_OFF_ALL_NOT_CU_RCT'
            self.acseq_ids[41]	= 'ACSEQ_SWITCH_OFF_AOCS_EQUIPMENTS'
            self.acseq_ids[39]	= 'ACSEQ_SWITCH_OFF_CASSIS'
            self.acseq_ids[190]	= 'ACSEQ_SWITCH_OFF_CTPU_AND_RTPU'
            self.acseq_ids[45]	= 'ACSEQ_SWITCH_OFF_FREND'
            self.acseq_ids[49]	= 'ACSEQ_SWITCH_OFF_NOMAD'
            self.acseq_ids[227]	= 'ACSEQ_SWITCH_OFF_PCDU_RCS_PROP_IF_AND_ME_IF'
            self.acseq_ids[241]	= 'ACSEQ_SWITCH_OFF_SAT_EQUIPMENTS_COMMON_PART'
            self.acseq_ids[40]	= 'ACSEQ_SWITCH_OFF_SMU_IO_PCDU_Core_RCS_PCU'
            self.acseq_ids[192]	= 'ACSEQ_SWITCH_ON_ALL_CU_RCT'
            self.acseq_ids[221]	= 'ACSEQ_SWITCH_ON_APM'
            self.acseq_ids[219]	= 'ACSEQ_SWITCH_ON_PCU_SAPR_PART_1'
            self.acseq_ids[193]	= 'ACSEQ_SWITCH_ON_PCU_SAPR_PART_2'
            self.acseq_ids[200]	= 'ACSEQ_SWITCH_ON_SADM'
            self.acseq_ids[38]	= 'ACSEQ_SWITCH_ON_SMU_IO_PCDU_Core_RCS_PCU'
            self.acseq_ids[151]	= 'ACSEQ_TCS_CONFIGURE_SETPOINT_FOR_LAUNCH_LEOP_CRUISE_PART_1'
            self.acseq_ids[152]	= 'ACSEQ_TCS_CONFIGURE_SETPOINT_FOR_LAUNCH_LEOP_CRUISE_PART_2'
            self.acseq_ids[224]	= 'ACSEQ_WAIT_FOR_SAM_SPIN_ENTRY'
            self.acseq_ids[43]	= 'ACSEQ_WAKE_UP'
            self.acseq_ids[164]	= 'ENTER_FAIL_OP'


    def source_code(self, dirname):

        action_sequence_code = dirname + '/fdir_m-core-action_seq.ads'
        action_sequence_ids = dirname + '/fdir_m-core-sdb.ads'


        f = open(action_sequence_ids)

        p = re.compile('FDIR_M\.([A-Z0-9_]+)\s*=>\s*([0-9]+)') 

        for line in f:
            entry = p.findall(line)
            for e in entry:
                self.acseq_ids[int(e[1])] = e[0]

        f.close()

        id = re.compile('ID => ([0-9]+)')
        d = re.compile('16#([0-9A-F][0-9A-F])#')
        f = open(action_sequence_code)
        bytes = [] 
        ID = ''

        for line in f:
            m1 = id.search(line.strip())
            m2 = d.findall(line.strip())
            if m1: 
                if len(bytes) > 0:
                    print ''
                    print '=========================================================================================================================================='
                    print 'Action Sequence ID =', ID, '-', self.acseq_ids[int(ID)]
                    print '=========================================================================================================================================='
                    self.process_data(bytes)
                    bytes = []
                if int(m1.groups()[0]) > 0:
                    ID = m1.groups()[0]
            elif len(m2) > 0:
                for b in m2:
                     bytes.append(int(b, 16))


        f.close()

    def s2k_obsm(self, filename):
    
        p = re.compile('DATA=([0-9A-F]+)')

        f = open(filename) 

        data = ''

        for line in f:
            m = p.search(line.strip())
            if m:
                data += m.groups()[0]

        f.close()

        bytes = []

        for i in range(0, len(data),2):
            bytes.append(int(data[i:i+2],16))

        self.process_data(bytes)

    def process_data(self, bytes):


        position = 0
        index = 1

        while position + 4 <= len(bytes):

            type = bytes[position] * 0x100 + bytes[position+1]
            length = bytes[position+2] * 0x100 + bytes[position+3]
            data = bytes[position+4:position+4+length]

            if length == 0:
                break

            position += 4 + length
 
            if type == 0:
                print 'INDEX = %(index)02d TYPE =%(type)5s : %(data)s' % {'index':index, 'type': 'CMD', 'data' : self.process_cmd(data)}
            elif type == 1:
                print 'INDEX = %(index)02d TYPE =%(type)5s : %(data)s' % {'index':index, 'type': 'WAIT', 'data' : str(self.int_32(data[0:4]))}
            elif type == 2:
                print 'INDEX = %(index)02d TYPE =%(type)5s : %(data)s' % {'index':index, 'type': 'ACSEQ', 'data' : 'ACQ(' + str(self.int_16(data[0:2])) + ') - ' + self.acseq_ids[int(data[1] + 0x100*data[0])]}
            elif type == 3:
                print 'INDEX = %(index)02d TYPE =%(type)5s : %(data)s' % {'index':index, 'type': 'CRIT', 'data' : 'Enter Critical Section'}
            elif type == 3:
                print 'INDEX = %(index)02d TYPE =%(type)5s : %(data)s' % {'index':index, 'type': 'CRIT', 'data' : 'Leave Critical Section'}
            else:
                print 'ERROR'
            index += 1

    def int_16(self,d):
        return 0x100 * d[0] + d[1]
    def int_32(self,d):
        return 0x1000000 * d[0] + 0x10000 * d[1] + 0x100 * d[2] + d[3]


    def process_cmd(self, data):
        type = data[7]
        subtype = data[8]

        text = 'TC(' + str(type) + ',' + str(subtype) + ') - '

        if type == 142 and subtype in [1,2]:
            N = self.int_16(data[10:12])
            fids = []
            for i in range(N):
                fids.append(str(self.int_32(data[12+i:16+i])))
            if subtype == 1:
                text += 'Enable FMON: '
            elif subtype == 2:
                text += 'Disable FMON: '
            text += ','.join(fids)

        elif type == 12 and subtype in [1,2,128,129]:
            N = self.int_16(data[10:12])
            fids = []
            for i in range(N):
                fids.append(str(self.int_32(data[12+i:16+i])))
            if subtype == 1:
                text += 'Enable PMON: '
            elif subtype == 2:
                text += 'Disable PMON: '
            elif subtype == 128:
                text += 'Enable temporary OOL: '
            elif subtype == 129:
                text += 'Disable temporary OOL: '
            text += ','.join(fids)

        elif type == 8 and subtype in [1, 128]:
            f = str(self.int_32(data[10:14]))
            if subtype == 1:
                text += 'Start Function: '
            elif subtype == 128:
                text += 'Stop Function: '
            text += f

        elif type == 11 and subtype in [1, 2, 6]:
            if subtype == 1:
                text += 'Enable MTL release'
            elif subtype == 2:
                text += 'Disable MTL release'
            elif subtype == 6:
                text += 'Delete MTL commands'

        elif type == 128 and subtype in [131]:
            if subtype == 131:
                param = self.int_32(data[10:14])
                if param == 0:
                    text += 'Re-init GNC Mode' 
                elif param == 1:
                    text += 'Re-init GNC Mode' 

        elif type == 129 and subtype in [128]:
            if subtype == 128:
                text += 'Set the function parameter value'
                    

        elif type == 171 and subtype in [1,2]:
            if subtype == 1:
                text += 'Enable Ground TC'
            elif subtype == 2:
                text += 'Disable Ground TC'

        elif type == 174 and subtype in [1,2,3,4]:
            if subtype == 1:
                text += 'PM Reconf Wathdog'
            elif subtype == 2:
                text += 'PM Reconf SW alarm'

            f = str(data[10])
            if subtype == 3:
                text += 'Enable PMON (Current use): '
            elif subtype == 4:
                text += 'Disable PMON (Current use): '
            text += f

        return text + ' ' + ''.join(['%(data)02X' % {'data':d} for d in data])

if __name__ == '__main__':
    main()
