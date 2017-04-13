import psrchive
import cPickle

def get_period(ar):
    p0 = ar.get_ephemeris().get_value("P0")
    if not p0:
        f0 = ar.get_ephemeris().get_value("F0")
        p0 = 1/float(f0)
    return float(p0)

def psrfits_to_pickle(fname,output_fname=None):
    ar = psrchive.Archive_load(fname)
    ar.dedisperse()
    ar.pscrunch()
    ar.remove_baseline()
    nsubint = int(ar.get_nsubint())
    tobs = nsubint * float(ar.get_Integration(0).get_duration())
    metadata = dict(
        source = ar.get_source(),
        period = get_period(ar),
        acceleration = 0.0,
        cfreq = ar.get_centre_frequency(),
        dm = ar.get_dispersion_measure(),
        bw = abs(ar.get_bandwidth()),
        nsubint = nsubint,
        nsubband = ar.get_nchan(),
        nphase = ar.get_nbin(),
        tobs = tobs,
        dc = 0.1,
        data = ar.get_data().squeeze()
    )
    metadata["chbw"] = metadata["bw"]/metadata["nsubband"] # the width in MHz of each frequency channel.
    metadata["tsub"] = metadata["tobs"]/metadata["nsubint"] # the width in seconds of each temporal bin.
    metadata["tphase"] = metadata["period"]/metadata["nphase"] # the width of each bin across the profile in seconds.
    if output_fname is None:
        stem = fname.split(".")[0]
        output_fname = "{0}.pickle".format(stem)
        print "Output file:",output_fname
    with open(output_fname,"w") as fout:
        cPickle.dump(metadata,fout)

if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser
    
    usage = "python {} <options>".format(sys.argv[0])
    parser = ArgumentParser(usage=usage)
    parser.add_argument("-i", "--input", type=str,
                        help="PSRFITS filename to convert",
                        required=True)
    parser.add_argument("-o", "--output", type=str,
                        help="Output pickle filename",
                        required=False, default=None)
    args = parser.parse_args()
    psrfits_to_pickle(args.input,args.output)
    

