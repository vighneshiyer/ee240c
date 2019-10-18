_V_MATLAB="${V_MATLAB:-2018a}"
_V_CDS="${V_CDS:-617}"
_V_CDS_BASE="${_V_CDS%%.*}" ###"$(expr "${_V_CDS}" : '\([^.]*\)')"
_V_ASSURA="${V_ASSURA:-41-${_V_CDS_BASE}}"
_V_MMSIM="${V_MMSIM:-171}"
_V_RC="${V_RC:-142}"
_V_EXT="${V_EXT:-171}"


add_cds_tool() {
  PATH=$PATH:$1/tools/bin
  if [ -e $1/tools/dfII/bin ]; then
    PATH=$PATH:$1/tools/dfII/bin
  fi
  MANPATH=$MANPATH:$1/share/man
}

[ -z "${CDS_LIC_FILE+1}" ] && CDS_LIC_FILE="5280@bisc.EECS.Berkeley.EDU"
export CDS_LIC_FILE

CDS_BASE="/share/instsww/cadence"

export CDS_INST_DIR="${CDS_BASE}/IC${_V_CDS}"
export CDS_INSTALL_DIR="${CDS_INST_DIR}/tools/dfII"

export ASSURA_INST_DIR="${CDS_BASE}/ASSURA${_V_ASSURA}"
export MMSIM_INST_DIR="${CDS_BASE}/MMSIM${_V_MMSIM}"
export RC_INST_DIR="${CDS_BASE}/RC${_V_RC}"
export EXT_INST_DIR="${CDS_BASE}/EXT${_V_EXT}"

export CDS_Netlisting_Mode="Analog"
export CDS_AUTO_64BIT="ALL"

if [ -z "${OA_UNSUPPORTED_PLAT+1}" -a -n \
     "$(lsb_release --description --short 2>/dev/null |egrep -i '^"?(Ubuntu|Cent.* release 7\.)')" \
   ]; then
  #NOTE: Ubuntu & CentOS 7 unsupported for IC616 and prior...also they use GCC4.8
  OA_UNSUPPORTED_PLAT="linux_rhel50_gcc44x" #TODO: linux_rhel40_gcc44x when <IC615!
  echo "WARN: Setting OA_UNSUPPORTED_PLAT='${OA_UNSUPPORTED_PLAT}'"
fi
export OA_HOME OA_UNSUPPORTED_PLAT


export ICHOME="${CDS_INST_DIR}"
export CDSHOME="${CDS_INST_DIR}"
export ICCHOME="${CDS_INST_DIR}"
export ASSURAHOME="${ASSURA_INST_DIR}"
export MMSIMHOME="${MMSIM_INST_DIR}"
export RCHOME="${RC_INST_DIR}"
export QRC_HOME="${EXT_INST_DIR}"

# 

add_cds_tool $RC_INST_DIR
add_cds_tool $MMSIM_INST_DIR
add_cds_tool $ASSURA_INST_DIR
add_cds_tool $CDS_INST_DIR

## Spectre toolbox for reading results with Matlab
_SPECTRE_MATLAB_="$(cds_root spectre)/tools/spectre/matlab/64bit"
if [ -d "${_SPECTRE_MATLAB_}" ]; then
  [ -z "${V_LIBS_KEEP+1}" ] && MATLABPATH=""
  MATLABPATH="${_SPECTRE_MATLAB_}${MATLABPATH:+:$MATLABPATH}"
  export MATLABPATH
  #LD_LIBRARY_PATH augmentation possibly not needed for newer MMSIMs
fi
