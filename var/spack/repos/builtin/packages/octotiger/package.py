class Octotiger(CMakePackage):
    """Astrophysics program simulating the evolution of star systems 
        based on the fast multipole method on adaptive Octrees"""

    homepage = "https://github.com/STEllAR-GROUP/octotiger"
    url = "https://github.com/STEllAR-GROUP/octotiger"

    # version('master', git='https://github.com/STEllAR-GROUP/hpx.git', branch='master')
    version('octotiger_with_kokkos', git='https://github.com/STEllAR-GROUP/octotiger.git',
        branch='octotiger_with_kokkos')

    variant('cuda', default=True, 
            description='Build octotiger fmm kernels with CUDA directly, not only the Kokkos/HPX parallel magic')

    #todo remove version numbers once this is stable enough
    depends_on('hpx@1.4.0+cuda cxxstd=14')
    depends_on('vc@1.4.1')
    depends_on('boost')
    depends_on('hdf5@:1.10.999 +mpi +cxx')
    depends_on('silo+mpi')#^hdf5+cxx+mpi')
    depends_on('kokkos @3.0 +serial +cuda +cuda_lambda +hpx +wrapper')#, when='@octotiger_with_kokkos') #cxxstd=c++14 # call e.g. for daint  with ^kokkos+pascal60+hsw 
    depends_on('kokkos-nvcc-wrapper', patches='Add-dumpversion-option-to-nvcc_wrapper.patch')
    depends_on('cmake@3.10:', type='build')
    depends_on('cuda', when='+cuda')

    def cmake_args(self):
        spec = self.spec
        args = []

        # Kokkos
        args.append('-DOCTOTIGER_WITH_KOKKOS={0}'.format(
            'ON' if '@octotiger_with_kokkos' else 'OFF'
        ))
        # set nvcc_wrapper as compiler
        args.append("-DCMAKE_CXX_COMPILER=%s" % self.spec["kokkos-nvcc-wrapper"].kokkos_cxx)

        return args
