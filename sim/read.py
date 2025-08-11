#convert the data from root to paranquet
import ROOT
import h5py
import numpy as np
import os
import sys

#helper function to assign data
def assign_data(dataset,data_list,index):
    if len(data_list)>0:
        dataset[index]=np.array(data_list)
    else:
        dataset[index]=np.array([])

#function to read the file
def read_root_file(root_file_path,hdf5_file_path):
    root_file = ROOT.TFile.Open(root_file_path,"READ")
    
    if not root_file or root_file.IsZombie():
        print("Error: Unable to open file!")
        return

    #Get the TTree
    tree = root_file.Get("events")

    if not tree:
        print("Error: Unable to retrive tree!")
        root_file.Close()
        return
    
    #Enable specific branch
    tree.SetBranchStatus("*",0)
    tree.SetBranchStatus("InnerTrackerBarrelCollection.*",1)
    tree.SetBranchStatus("VertexBarrelCollection.*",1)
    #tree.SetBranchStatus("InnerTrackerEndcapCollection.*",1)
    #tree.SetBranchStatus("PandoraPFOs.*",1)
    tree.SetBranchStatus("MCParticles.*",1)
    tree.SetBranchStatus("OuterTrackerBarrelCollection.*",1)
    #tree.SetBranchStatus("SiTracks.*",1)
    #tree.SetBranchStatus("_SiTracks_trackStates.*",1)

    #Declare variable to hold branch data
    innerTrackerBarrelCollection = ROOT.std.vector("edm4hep::SimTrackerHitData")()
    vertexBarrelCollection = ROOT.std.vector("edm4hep::SimTrackerHitData")()
    #pandoraPFOs = ROOT.std.vector("edm4hep::ReconstructedParticleData")()
    mcParticles = ROOT.std.vector("edm4hep::MCParticleData")()
    outerTrackerBarrelCollection = ROOT.std.vector("edm4hep::SimTrackerHitData")()
    #siTracks = ROOT.std.vector("edm4hep::TrackData")()
    #siTracks_trackStates = ROOT.std.vector("edm4hep::TrackState")()


    #Set branch address
    tree.SetBranchAddress("InnerTrackerBarrelCollection",innerTrackerBarrelCollection)
    tree.SetBranchAddress("VertexBarrelCollection",vertexBarrelCollection)
    #tree.SetBranchAddress("InnerTrackerEndcapCollection",innerTrackerBarrelCollection)
    #tree.SetBranchAddress("PandoraPFOs", pandoraPFOs)
    tree.SetBranchAddress("MCParticles",mcParticles)
    tree.SetBranchAddress("OuterTrackerBarrelCollection",outerTrackerBarrelCollection)
    #tree.SetBranchAddress("SiTracks",siTracks)
    #tree.SetBranchAddress("_SiTracks_trackStates",siTracks_trackStates)

    #Open HDF5 file
    with h5py.File(hdf5_file_path,"w") as hdf5_file:
    
        #create groups
        innerTracker_gr = hdf5_file.create_group("InnerTrackerBarrelCollection")
        vertexTracker_gr = hdf5_file.create_group("VertexBarrelCollection")
        #innerTracker_gr = hdf5_file.create_group("InnerTrackerEndcapCollection")
        #pandora_gr = hdf5_file.create_group("PandoraPFOs")
        mcparticle_gr = hdf5_file.create_group("MCParticles")
        outerTracker_gr = hdf5_file.create_group("OuterTrackerBarrelCollection")
        #siTrack_gr = hdf5_file.create_group("SiTracks")
        #siTracks_trackStates_gr = hdf5_file.create_group("_SiTracks_trackStates")

        #define variable length data types
        vlen_int = h5py.vlen_dtype(np.int32)
        vlen_float = h5py.vlen_dtype(np.float32)

        #create datasets for InnerTrackerBarrelCollection
        cellID = innerTracker_gr.create_dataset("cellID",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        eDep = innerTracker_gr.create_dataset("eDep",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        time = innerTracker_gr.create_dataset("time",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        pathLength = innerTracker_gr.create_dataset("pathLength",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        quality = innerTracker_gr.create_dataset("quality",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        positionX = innerTracker_gr.create_dataset("positionX",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        positionY = innerTracker_gr.create_dataset("positionY",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        positionZ = innerTracker_gr.create_dataset("positionZ",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momentumX = innerTracker_gr.create_dataset("momentumX",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momentumY = innerTracker_gr.create_dataset("momentumY",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momentumZ = innerTracker_gr.create_dataset("momentumZ",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        
        #create datasets for vertexBarrelCollection
        cellID_v = vertexTracker_gr.create_dataset("cellID",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        eDep_v = vertexTracker_gr.create_dataset("eDep",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        time_v = vertexTracker_gr.create_dataset("time",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        pathLength_v = vertexTracker_gr.create_dataset("pathLength",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        quality_v = vertexTracker_gr.create_dataset("quality",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        positionX_v = vertexTracker_gr.create_dataset("positionX",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        positionY_v = vertexTracker_gr.create_dataset("positionY",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        positionZ_v = vertexTracker_gr.create_dataset("positionZ",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momentumX_v = vertexTracker_gr.create_dataset("momentumX",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momentumY_v = vertexTracker_gr.create_dataset("momentumY",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momentumZ_v = vertexTracker_gr.create_dataset("momentumZ",shape=(10000,),maxshape=(None,),dtype=vlen_float)

        #create datasets for PandoraPFOs
        '''
        PDG_pfo = pandora_gr.create_dataset("PDG",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        energy_pfo = pandora_gr.create_dataset("energy",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momX_pfo = pandora_gr.create_dataset("momentumX",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momY_pfo = pandora_gr.create_dataset("momentumY",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momZ_pfo = pandora_gr.create_dataset("momentumZ",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        refX_pfo = pandora_gr.create_dataset("referencePointX",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        refY_pfo = pandora_gr.create_dataset("referencePointY",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        refZ_pfo = pandora_gr.create_dataset("referencePointZ",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        charge_pfo = pandora_gr.create_dataset("charge",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        mass_pfo = pandora_gr.create_dataset("mass",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        cls_begin = pandora_gr.create_dataset("cluster_begin",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        cls_end = pandora_gr.create_dataset("cluster_end",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        trk_begin = pandora_gr.create_dataset("tracks_begin",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        trk_end = pandora_gr.create_dataset("tracks_end",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        par_begin = pandora_gr.create_dataset("particles_begin",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        par_end = pandora_gr.create_dataset("particles_end",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        '''

        #create dataset for MCParticles
        pdg_mc = mcparticle_gr.create_dataset("PDG",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        genStatus_mc = mcparticle_gr.create_dataset("generatorStatus",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        simStatus_mc = mcparticle_gr.create_dataset("simulatorStatusDG",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        charge_mc = mcparticle_gr.create_dataset("charge",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        time_mc = mcparticle_gr.create_dataset("time",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        mass_mc = mcparticle_gr.create_dataset("mass",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        verX_mc = mcparticle_gr.create_dataset("vertex.x",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        verY_mc = mcparticle_gr.create_dataset("vertex.y",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        verZ_mc = mcparticle_gr.create_dataset("vertex.z",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        endX_mc = mcparticle_gr.create_dataset("endpoint.x",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        endY_mc = mcparticle_gr.create_dataset("endpoint.y",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        endZ_mc = mcparticle_gr.create_dataset("endpoint.z",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momX_mc = mcparticle_gr.create_dataset("momentum.x",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momY_mc = mcparticle_gr.create_dataset("momentum.y",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momZ_mc = mcparticle_gr.create_dataset("momentum.z",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momEndX_mc = mcparticle_gr.create_dataset("momentumAtEndpoint.x",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momEndY_mc = mcparticle_gr.create_dataset("momentumAtEndpoint.y",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momEndZ_mc = mcparticle_gr.create_dataset("momentumAtEndpoint.z",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        par_begin_mc = mcparticle_gr.create_dataset("parents_begin",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        par_end_mc = mcparticle_gr.create_dataset("parents_end",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        daug_begin_mc = mcparticle_gr.create_dataset("daughters_begin",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        daug_end_mc = mcparticle_gr.create_dataset("daughters_end",shape=(10000,),maxshape=(None,),dtype=vlen_int)

        #create datasets for OuterTrackerBarrelCollection
        cellID_out = outerTracker_gr.create_dataset("cellID",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        eDep_out = outerTracker_gr.create_dataset("eDep",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        time_out = outerTracker_gr.create_dataset("time",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        pathLength_out = outerTracker_gr.create_dataset("pathLength",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        quality_out = outerTracker_gr.create_dataset("quality",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        positionX_out = outerTracker_gr.create_dataset("positionX",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        positionY_out = outerTracker_gr.create_dataset("positionY",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        positionZ_out = outerTracker_gr.create_dataset("positionZ",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momentumX_out = outerTracker_gr.create_dataset("momentumX",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momentumY_out = outerTracker_gr.create_dataset("momentumY",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        momentumZ_out = outerTracker_gr.create_dataset("momentumZ",shape=(10000,),maxshape=(None,),dtype=vlen_float)


        #create datasets for SiTracks
        '''
        type_stk = siTrack_gr.create_dataset("type",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        chi2_stk = siTrack_gr.create_dataset("chi2",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        ndf_stk = siTrack_gr.create_dataset("ndf",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        tks_begin_stk = siTrack_gr.create_dataset("trackStates_begin",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        tks_end_stk = siTrack_gr.create_dataset("trackStates_end",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        tks_hit_begin_stk = siTrack_gr.create_dataset("trackerHits_begin",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        tks_hit_end_stk = siTrack_gr.create_dataset("trackerHits_end",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        track_begin_stk = siTrack_gr.create_dataset("tracks_begin",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        track_end_stk = siTrack_gr.create_dataset("tracks_end",shape=(10000,),maxshape=(None,),dtype=vlen_int)


        #create datasets for _SiTracks_trackStates
        loc_siTrk_states = siTracks_trackStates_gr.create_dataset("location",shape=(10000,),maxshape=(None,),dtype=vlen_int)
        D0_siTrk_states = siTracks_trackStates_gr.create_dataset("D0",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        phi_siTrk_states = siTracks_trackStates_gr.create_dataset("phi",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        omega_siTrk_states = siTracks_trackStates_gr.create_dataset("omega",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        Z0_siTrk_states = siTracks_trackStates_gr.create_dataset("Z0",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        tanLambda_siTrk_states = siTracks_trackStates_gr.create_dataset("tanLambda",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        time_siTrk_states = siTracks_trackStates_gr.create_dataset("time",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        referencePointX_siTrk_states = siTracks_trackStates_gr.create_dataset("referencePoint.x",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        referencePointY_siTrk_states = siTracks_trackStates_gr.create_dataset("referencePoint.y",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        referencePointZ_siTrk_states = siTracks_trackStates_gr.create_dataset("referencePoint.z",shape=(10000,),maxshape=(None,),dtype=vlen_float)
        '''

        #Loop over entries
        entries = tree.GetEntries()
        print('entries: ', entries)

        #Loop through each entry in root file
        for i in range(tree.GetEntries()):
            tree.GetEntry(i)

            #Process Innertracker data
            if innerTrackerBarrelCollection:
                cell_idHit = [hit.cellID for hit in innerTrackerBarrelCollection]
                eDepHit = [hit.eDep for hit in innerTrackerBarrelCollection]
                timeHit = [hit.time for hit in innerTrackerBarrelCollection]
                pathLengthHit = [hit.pathLength for hit in innerTrackerBarrelCollection]
                qualityHit = [hit.quality for hit in innerTrackerBarrelCollection]
                pos_xHit = [hit.position.x for hit in innerTrackerBarrelCollection]
                pos_yHit = [hit.position.y for hit in innerTrackerBarrelCollection]
                pos_zHit = [hit.position.z for hit in innerTrackerBarrelCollection]
                mom_xHit = [hit.momentum.x for hit in innerTrackerBarrelCollection]
                mom_yHit = [hit.momentum.y for hit in innerTrackerBarrelCollection]
                mom_zHit = [hit.momentum.z for hit in innerTrackerBarrelCollection]

                #print(f"Entry: {i} and x-momentum: {mom_xHit}")

                #append the data
                assign_data(cellID,cell_idHit,i)
                assign_data(eDep,eDepHit,i)
                assign_data(time,timeHit,i)
                assign_data(pathLength,pathLengthHit,i)
                assign_data(quality,qualityHit,i)
                assign_data(positionX,pos_xHit,i)
                assign_data(positionY,pos_yHit,i)
                assign_data(positionZ,pos_zHit,i)
                assign_data(momentumX,mom_xHit,i)
                assign_data(momentumY,mom_yHit,i)
                assign_data(momentumZ,mom_zHit,i)

            else:
                assign_data(cellID,[],i)
                assign_data(eDep,[],i)
                assign_data(time,[],i)
                assign_data(pathLength,[],i)
                assign_data(quality,[],i)
                assign_data(positionX,[],i)
                assign_data(positionY,[],i)
                assign_data(positionZ,[],i)
                assign_data(momentumX,[],i)
                assign_data(momentumY,[],i)
                assign_data(momentumZ,[],i)

            #Process vertexBarrelCollection data
            if vertexBarrelCollection:
                cell_idHit_v = [hit.cellID for hit in vertexBarrelCollection]
                eDepHit_v = [hit.eDep for hit in vertexBarrelCollection]
                timeHit_v = [hit.time for hit in vertexBarrelCollection]
                pathLengthHit_v = [hit.pathLength for hit in vertexBarrelCollection]
                qualityHit_v = [hit.quality for hit in vertexBarrelCollection]
                pos_xHit_v = [hit.position.x for hit in vertexBarrelCollection]
                pos_yHit_v = [hit.position.y for hit in vertexBarrelCollection]
                pos_zHit_v = [hit.position.z for hit in vertexBarrelCollection]
                mom_xHit_v = [hit.momentum.x for hit in vertexBarrelCollection]
                mom_yHit_v = [hit.momentum.y for hit in vertexBarrelCollection]
                mom_zHit_v = [hit.momentum.z for hit in vertexBarrelCollection]
                

                #print(f"Entry: {i} and x-momentum in vertex: {mom_xHit_v}")

                #append the data
                assign_data(cellID_v,cell_idHit_v,i)
                assign_data(eDep_v,eDepHit_v,i)
                assign_data(time_v,timeHit_v,i)
                assign_data(pathLength_v,pathLengthHit_v,i)
                assign_data(quality_v,qualityHit_v,i)
                assign_data(positionX_v,pos_xHit_v,i)
                assign_data(positionY_v,pos_yHit_v,i)
                assign_data(positionZ_v,pos_zHit_v,i)
                assign_data(momentumX_v,mom_xHit_v,i)
                assign_data(momentumY_v,mom_yHit_v,i)
                assign_data(momentumZ_v,mom_zHit_v,i)

            else:
                assign_data(cellID_v,[],i)
                assign_data(eDep_v,[],i)
                assign_data(time_v,[],i)
                assign_data(pathLength_v,[],i)
                assign_data(quality_v,[],i)
                assign_data(positionX_v,[],i)
                assign_data(positionY_v,[],i)
                assign_data(positionZ_v,[],i)
                assign_data(momentumX_v,[],i)
                assign_data(momentumY_v,[],i)
                assign_data(momentumZ_v,[],i)
            #Process PandoraPFOs data
            '''
            if pandoraPFOs:
                pdg_hit = [hit.PDG for hit in pandoraPFOs]
                energy_hit = [hit.energy for hit in pandoraPFOs]
                momX_hit = [hit.momentum.x for hit in pandoraPFOs]
                momY_hit = [hit.momentum.y for hit in pandoraPFOs]
                momZ_hit = [hit.momentum.z for hit in pandoraPFOs]
                refX_hit = [hit.referencePoint.x for hit in pandoraPFOs]
                refY_hit = [hit.referencePoint.y for hit in pandoraPFOs]
                refZ_hit = [hit.referencePoint.z for hit in pandoraPFOs]
                charge_hit = [hit.charge for hit in pandoraPFOs]
                mass_hit = [hit.mass for hit in pandoraPFOs]
                cls_begin_hit = [hit.clusters_begin for hit in pandoraPFOs]
                cls_end_hit = [hit.clusters_end for hit in pandoraPFOs]
                trk_begin_hit = [hit.tracks_begin for hit in pandoraPFOs]
                trk_end_hit = [hit.tracks_begin for hit in pandoraPFOs]
                par_begin_hit = [hit.particles_begin for hit in pandoraPFOs]
                par_end_hit = [hit.particles_end for hit in pandoraPFOs]

                #append the data
                assign_data(PDG_pfo,pdg_hit,i)
                assign_data(energy_pfo,energy_hit,i)
                assign_data(momX_pfo,momX_hit,i)
                assign_data(momY_pfo,momY_hit,i)
                assign_data(momZ_pfo,momZ_hit,i)
                assign_data(refX_pfo,refX_hit,i)
                assign_data(refY_pfo,refY_hit,i)
                assign_data(refZ_pfo,refZ_hit,i)
                assign_data(charge_pfo,charge_hit,i)
                assign_data(mass_pfo,mass_hit,i)
                assign_data(cls_begin,cls_begin_hit,i)
                assign_data(cls_end,cls_end_hit,i)
                assign_data(trk_begin,trk_begin_hit,i)
                assign_data(trk_end,trk_end_hit,i)
                assign_data(par_begin,par_begin_hit,i)
                assign_data(par_end,par_end_hit,i)

            else:
                assign_data(PDG_pfo,[],i)
                assign_data(energy_pfo,[],i)
                assign_data(momX_pfo,[],i)
                assign_data(momY_pfo,[],i)
                assign_data(momZ_pfo,[],i)
                assign_data(refX_pfo,[],i)
                assign_data(refY_pfo,[],i)
                assign_data(refZ_pfo,[],i)
                assign_data(charge_pfo,[],i)
                assign_data(mass_pfo,[],i)
                assign_data(cls_begin,[],i)
                assign_data(cls_end,[],i)
                assign_data(trk_begin,[],i)
                assign_data(trk_end,[],i)
                assign_data(par_begin,[],i)
                assign_data(par_end,[],i)
            '''
            
            #process MCParticles data
            if mcParticles:
                pdg_mc_hit = [hit.PDG for hit in mcParticles]
                genStatus_mc_hit = [hit.generatorStatus for hit in mcParticles]
                simStatus_mc_hit = [hit.simulatorStatus for hit in mcParticles]
                charge_mc_hit = [hit.charge for hit in mcParticles]
                time_mc_hit = [hit.time for hit in mcParticles]
                mass_mc_hit = [hit.mass for hit in mcParticles]
                verX_mc_hit = [hit.vertex.x for hit in mcParticles]
                verY_mc_hit = [hit.vertex.y for hit in mcParticles]
                verZ_mc_hit = [hit.vertex.z for hit in mcParticles]
                endX_mc_hit = [hit.endpoint.x for hit in mcParticles]
                endY_mc_hit = [hit.endpoint.y for hit in mcParticles]
                endZ_mc_hit = [hit.endpoint.z for hit in mcParticles]
                momX_mc_hit = [hit.momentum.x for hit in mcParticles]
                momY_mc_hit = [hit.momentum.y for hit in mcParticles]
                momZ_mc_hit = [hit.momentum.z for hit in mcParticles]
                momEndX_mc_hit = [hit.momentumAtEndpoint.x for hit in mcParticles]
                momEndY_mc_hit = [hit.momentumAtEndpoint.y for hit in mcParticles]
                momEndZ_mc_hit = [hit.momentumAtEndpoint.z for hit in mcParticles]
                par_begin_mc_hit = [hit.parents_begin for hit in mcParticles]
                par_end_mc_hit = [hit.parents_end for hit in mcParticles]
                daug_begin_mc_hit = [hit.daughters_begin for hit in mcParticles]
                daug_end_mc_hit= [hit.daughters_end for hit in mcParticles]

                #append data
                assign_data(pdg_mc,pdg_mc_hit,i)
                assign_data(genStatus_mc,genStatus_mc_hit,i)
                assign_data(simStatus_mc,simStatus_mc_hit,i)
                assign_data(charge_mc,charge_mc_hit,i)
                assign_data(time_mc, time_mc_hit,i)
                assign_data(mass_mc,mass_mc_hit,i)
                assign_data(verX_mc,verX_mc_hit,i)
                assign_data(verY_mc,verY_mc_hit,i)
                assign_data(verZ_mc,verZ_mc_hit,i)
                assign_data(endX_mc,endX_mc_hit,i)
                assign_data(endY_mc,endY_mc_hit,i)
                assign_data(endZ_mc,endZ_mc_hit,i)
                assign_data(momX_mc,momX_mc_hit,i)
                assign_data(momY_mc,momY_mc_hit,i)
                assign_data(momZ_mc,momZ_mc_hit,i)
                assign_data(momEndX_mc,momEndX_mc_hit,i)
                assign_data(momEndY_mc,momEndY_mc_hit,i)
                assign_data(momEndZ_mc,momEndZ_mc_hit,i)
                assign_data(par_begin_mc,par_begin_mc_hit,i)
                assign_data(par_end_mc,par_end_mc_hit,i)
                assign_data(daug_begin_mc,daug_begin_mc_hit,i)
                assign_data(daug_end_mc,daug_end_mc_hit,i)

            else:
                assign_data(pdg_mc,[],i)
                assign_data(genStatus_mc,[],i)
                assign_data(simStatus_mc,[],i)
                assign_data(charge_mc,[],i)
                assign_data(time_mc, [],i)
                assign_data(mass_mc,[],i)
                assign_data(verX_mc,[],i)
                assign_data(verY_mc,[],i)
                assign_data(verZ_mc,[],i)
                assign_data(endX_mc,[],i)
                assign_data(endY_mc,[],i)
                assign_data(endZ_mc,[],i)
                assign_data(momX_mc,[],i)
                assign_data(momY_mc,[],i)
                assign_data(momZ_mc,[],i)
                assign_data(momEndX_mc,[],i)
                assign_data(momEndY_mc,[],i)
                assign_data(momEndZ_mc,[],i)
                assign_data(par_begin_mc,[],i)
                assign_data(par_end_mc,[],i)
                assign_data(daug_begin_mc,[],i)
                assign_data(daug_end_mc,[],i)

            #process OuterTracker data
            if outerTrackerBarrelCollection:
                cell_idHit_out = [hit.cellID for hit in outerTrackerBarrelCollection]
                eDepHit_out = [hit.eDep for hit in outerTrackerBarrelCollection]
                timeHit_out = [hit.time for hit in outerTrackerBarrelCollection]
                pathLengthHit_out = [hit.pathLength for hit in outerTrackerBarrelCollection]
                qualityHit_out = [hit.quality for hit in outerTrackerBarrelCollection]
                pos_xHit_out = [hit.position.x for hit in outerTrackerBarrelCollection]
                pos_yHit_out = [hit.position.y for hit in outerTrackerBarrelCollection]
                pos_zHit_out = [hit.position.z for hit in outerTrackerBarrelCollection]
                mom_xHit_out = [hit.momentum.x for hit in outerTrackerBarrelCollection]
                mom_yHit_out = [hit.momentum.y for hit in outerTrackerBarrelCollection]
                mom_zHit_out = [hit.momentum.z for hit in outerTrackerBarrelCollection]

                #print("data: ",mom_xHit_out)

                #append the data
                assign_data(cellID_out,cell_idHit_out,i)
                assign_data(eDep_out,eDepHit_out,i)
                assign_data(time_out,timeHit_out,i)
                assign_data(pathLength_out,pathLengthHit_out,i)
                assign_data(quality_out,qualityHit_out,i)
                assign_data(positionX_out,pos_xHit_out,i)
                assign_data(positionY_out,pos_yHit_out,i)
                assign_data(positionZ_out,pos_zHit_out,i)
                assign_data(momentumX_out,mom_xHit_out,i)
                assign_data(momentumY_out,mom_yHit_out,i)
                assign_data(momentumZ_out,mom_zHit_out,i)
            else:
                assign_data(cellID_out,[],i)
                assign_data(eDep_out,[],i)
                assign_data(time_out,[],i)
                assign_data(pathLength_out,[],i)
                assign_data(quality_out,[],i)
                assign_data(positionX_out,[],i)
                assign_data(positionY_out,[],i)
                assign_data(positionZ_out,[],i)
                assign_data(momentumX_out,[],i)
                assign_data(momentumY_out,[],i)
                assign_data(momentumZ_out,[],i)

            #process SiTracks data
            '''
            if siTracks:
                type_stk_hit = [hit.type for hit in siTracks]
                chi2_stk_hit = [hit.chi2 for hit in siTracks]
                ndf_stk_hit = [hit.ndf for hit in siTracks]
                tks_begin_stk_hit = [hit.trackStates_begin for hit in siTracks]
                tks_end_stk_hit = [hit.trackStates_end for hit in siTracks]
                tks_hit_begin_stk_hit = [hit.trackerHits_begin for hit in siTracks]
                tks_hit_end_stk_hit = [hit.trackerHits_end for hit in siTracks]
                track_begin_stk_hit = [hit.tracks_begin for hit in siTracks]
                track_end_stk_hit = [hit.tracks_end for hit in siTracks]

                #append the data
                assign_data(type_stk,type_stk_hit,i)
                assign_data(chi2_stk,chi2_stk_hit,i)
                assign_data(ndf_stk,ndf_stk_hit,i)
                assign_data(tks_begin_stk,tks_begin_stk_hit,i)
                assign_data(tks_end_stk,tks_end_stk_hit,i)
                assign_data(tks_hit_begin_stk,tks_hit_begin_stk_hit,i)
                assign_data(tks_hit_end_stk,tks_hit_end_stk_hit,i)
                assign_data(track_begin_stk,track_begin_stk_hit,i)
                assign_data(track_end_stk,track_end_stk_hit,i)

            else:
                assign_data(type_stk,[],i)
                assign_data(chi2_stk,[],i)
                assign_data(ndf_stk,[],i)
                assign_data(tks_begin_stk,[],i)
                assign_data(tks_end_stk,[],i)
                assign_data(tks_hit_begin_stk,[],i)
                assign_data(tks_hit_end_stk,[],i)
                assign_data(track_begin_stk,[],i)
                assign_data(track_end_stk,[],i)

            
            #process _SiTracks_trackStates
            if siTracks_trackStates:
                loc_siTrk_states_hit = [hit.location for hit in siTracks_trackStates]
                D0_siTrk_states_hit = [hit.D0 for hit in siTracks_trackStates]
                phi_siTrk_states_hit = [hit.phi for hit in siTracks_trackStates]
                omega_siTrk_states_hit = [hit.omega for hit in siTracks_trackStates]
                Z0_siTrk_states_hit = [hit.Z0 for hit in siTracks_trackStates]
                tanLambda_siTrk_states_hit = [hit.tanLambda for hit in siTracks_trackStates]
                time_siTrk_states_hit = [hit.time for hit in siTracks_trackStates]
                referencePointX_siTrk_states_hit = [hit.referencePoint.x for hit in siTracks_trackStates]
                referencePointY_siTrk_states_hit = [hit.referencePoint.y for hit in siTracks_trackStates]
                referencePointZ_siTrk_states_hit = [hit.referencePoint.z for hit in siTracks_trackStates]


                #append data
                assign_data(loc_siTrk_states,loc_siTrk_states_hit,i)
                assign_data(D0_siTrk_states,D0_siTrk_states_hit,i)
                assign_data(phi_siTrk_states,phi_siTrk_states_hit,i)
                assign_data(omega_siTrk_states,omega_siTrk_states_hit,i)
                assign_data(Z0_siTrk_states,Z0_siTrk_states_hit,i)
                assign_data(tanLambda_siTrk_states,tanLambda_siTrk_states_hit,i)
                assign_data(time_siTrk_states,time_siTrk_states_hit,i)
                assign_data(referencePointX_siTrk_states,referencePointX_siTrk_states_hit,i)
                assign_data(referencePointY_siTrk_states,referencePointY_siTrk_states_hit,i)
                assign_data(referencePointZ_siTrk_states,referencePointZ_siTrk_states_hit,i)

            else:
                assign_data(loc_siTrk_states,[],i)
                assign_data(D0_siTrk_states,[],i)
                assign_data(phi_siTrk_states,[],i)
                assign_data(omega_siTrk_states,[],i)
                assign_data(Z0_siTrk_states,[],i)
                assign_data(tanLambda_siTrk_states,[],i)
                assign_data(time_siTrk_states,[],i)
                assign_data(referencePointX_siTrk_states,[],i)
                assign_data(referencePointY_siTrk_states,[],i)
                assign_data(referencePointZ_siTrk_states,[],i)

            '''

    print(f"Data successfully saved")




if __name__ == "__main__":

    # #file
    #root_file_path = "../data/CLD_SINGLE_PAR/sergei.edm4hep.root"
    
    root_file_path = "./muMinus45degree_10gev_CLD.root"
    
    file_name = os.path.splitext(os.path.basename(root_file_path))[0]
    
    hdf5_file_path = f"{file_name}.hdf5"

    read_root_file(root_file_path,hdf5_file_path)

    '''
    #automate for all files from the script
    if len(sys.argv)!=2:
        print("Usage: wrong arguments for python read.py")
        sys.exit(1)

    #get the root file path from command-line
    root_file_path = sys.argv[1]

    #filename without extension
    file_name = os.path.splitext(os.path.basename(root_file_path))[0]

    #hdf5 filename
    hdf5_file_path = f"{file_name}.hdf5"

    read_root_file(root_file_path,hdf5_file_path)
    '''



