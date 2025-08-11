#! /usr/bin/bash

COMPACT_FILE=$K4GEO/FCCee/CLD/compact/CLD_o2_v07/CLD_o2_v07.xml
PARTICLE=mu-
NEVT=10000
HANDLER=TV

ddsim --compactFile $COMPACT_FILE \
      --outputFile sergei.$PARTICLE.$NEVT.$HANDLER.SIM.edm4hep.root \
      --steeringFile $CLDCONFIG/share/CLDConfig/cld_steer.py \
      --part.userParticleHandler Geant4${HANDLER}UserParticleHandler \
      --numberOfEvents $NEVT \
      --enableGun \
      --gun.particle=$PARTICLE \
      --gun.distribution=uniform  \
      --gun.momentumMin=10*GeV \
      --gun.momentumMax=10*GeV \
      --gun.thetaMin=45*deg \
      --gun.thetaMax=45*deg \
      --random.seed 1796357082 \
      --crossingAngleBoost=0
