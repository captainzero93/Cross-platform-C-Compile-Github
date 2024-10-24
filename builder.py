from pathlib import Path
import subprocess
import platform
import shutil
import sys
import os
import time

class WindowsTools:
    @staticmethod
    def get_vs_install_path():
        """Get Visual Studio installation path using vswhere"""
        program_files = os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)')
        vswhere = os.path.join(program_files, 'Microsoft Visual Studio', 'Installer', 'vswhere.exe')
        
        if not os.path.exists(vswhere):
            return None
            
        try:
            result = subprocess.run([
                vswhere,
                '-latest',
                '-products', '*',
                '-requires', 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64',
                '-property', 'installationPath'
            ], capture_output=True, text=True)
            
            return result.stdout.strip()
        except Exception:
            return None
    
    @staticmethod
    def find_msbuild():
        """Find MSBuild.exe in various possible locations"""
        vs_path = WindowsTools.get_vs_install_path()
        if vs_path:
            msbuild_path = os.path.join(vs_path, 'MSBuild', 'Current', 'Bin', 'MSBuild.exe')
            if os.path.exists(msbuild_path):
                return msbuild_path
        
        common_paths = [
            r'C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe',
            r'C:\Program Files\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe',
            r'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\MSBuild.exe',
            r'C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\MSBuild\Current\Bin\MSBuild.exe',
            r'C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\MSBuild.exe',
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None

class BuildSystem:
    CMAKE = "cmake"
    MAKE = "make"
    AUTOTOOLS = "autotools"
    UNKNOWN = "unknown"

class CProjectBuilder:
    def __init__(self, github_url, branch=None):
        self.github_url = github_url
        self.branch = branch
        self.project_root = Path(__file__).parent
        self.project_name = github_url.split('/')[-1].replace('.git', '')
        self.source_dir = self.project_root / 'source' / self.project_name
        self.build_dir = self.project_root / 'build' / self.project_name
        self.output_dir = self.project_root / 'output' / self.project_name
        self.msbuild_path = None if platform.system() == 'Windows' else None
        self.build_system = None

    def detect_build_system(self):
        """Detect which build system the project uses"""
        print("\nDetecting build system...")
        
        # Check for CMake
        if (self.source_dir / "CMakeLists.txt").exists():
            print("✓ CMake build system detected")
            return BuildSystem.CMAKE
        
        # Check for Autotools
        if (self.source_dir / "configure.ac").exists() or (self.source_dir / "configure").exists():
            print("✓ Autotools build system detected")
            return BuildSystem.AUTOTOOLS
        
        # Check for Make
        if (self.source_dir / "Makefile").exists() or list(self.source_dir.glob("makefile*")):
            print("✓ Make build system detected")
            return BuildSystem.MAKE
        
        print("! No recognized build system detected")
        return BuildSystem.UNKNOWN

    def check_dependencies(self):
        """Check if required build tools are available"""
        print("Checking build dependencies...")
        missing_tools = []
        
        # Check for Git
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            print("✓ Git found")
        except (subprocess.SubprocessError, FileNotFoundError):
            missing_tools.append('git')
            if platform.system() == 'Windows':
                print("""
Git not found! Please install:
1. Download from: https://git-scm.com/download/win
2. Run installer and select "Add to PATH"
""")
            else:
                print("Git not found! Please install using your package manager.")

        # Check for Make
        try:
            subprocess.run(['make', '--version'], capture_output=True, check=True)
            print("✓ Make found")
        except (subprocess.SubprocessError, FileNotFoundError):
            missing_tools.append('make')
            if platform.system() == 'Windows':
                print("Make not found! Please install MinGW or Cygwin.")
            else:
                print("Make not found! Please install using your package manager.")

        # Check for CMake
        try:
            subprocess.run(['cmake', '--version'], capture_output=True, check=True)
            print("✓ CMake found")
        except (subprocess.SubprocessError, FileNotFoundError):
            missing_tools.append('cmake')
            if platform.system() == 'Windows':
                print("""
CMake not found! Please install:
1. Download from: https://cmake.org/download/
2. Choose Windows x64 Installer
3. During installation, select "Add CMake to system PATH"
""")
            else:
                print("CMake not found! Please install using your package manager.")

        # Windows-specific checks
        if platform.system() == 'Windows':
            self.msbuild_path = WindowsTools.find_msbuild()
            if not self.msbuild_path:
                missing_tools.append('msbuild')
                print("""
Visual Studio Build Tools not found! Please install:
1. Download Visual Studio Build Tools 2022:
   https://aka.ms/vs/17/release/vs_buildtools.exe
   
2. Run the installer and select:
   - "Desktop development with C++"
   Including these components:
   - MSVC Build Tools
   - Windows 10/11 SDK
   - C++ CMake tools
   
3. Complete installation and restart your computer
""")
            else:
                print(f"✓ MSBuild found at: {self.msbuild_path}")
                
        return missing_tools

    def clean_directories(self):
        """Clean the build and output directories"""
        print("\nCleaning directories...")
        for directory in [self.build_dir, self.output_dir]:
            if directory.exists():
                shutil.rmtree(str(directory))
                time.sleep(1)
            directory.mkdir(parents=True, exist_ok=True)
        print("✓ Directories cleaned")

    def clone_repository(self):
        """Clone the specified GitHub repository"""
        print(f"\nCloning repository from {self.github_url}...")
        
        if self.source_dir.exists():
            shutil.rmtree(str(self.source_dir))
            time.sleep(1)
        
        cmd = ['git', 'clone']
        if self.branch:
            cmd.extend(['--branch', self.branch])
        cmd.extend([self.github_url, str(self.source_dir)])
        
        subprocess.run(cmd, check=True)
        
        # Initialize and update submodules
        subprocess.run(['git', 'submodule', 'update', '--init', '--recursive'], 
                     cwd=str(self.source_dir), check=True)
        print("✓ Repository and submodules cloned successfully")

    def build_cmake_project(self):
        """Build project using CMake"""
        print("\nBuilding with CMake...")
        
        cmake_args = [
            'cmake',
            '-S', str(self.source_dir),
            '-B', str(self.build_dir),
        ]
        
        if platform.system() == 'Windows':
            cmake_args.extend([
                '-A', 'x64',
                '-DCMAKE_INSTALL_PREFIX=' + str(self.output_dir)
            ])
        else:
            cmake_args.extend([
                '-DCMAKE_BUILD_TYPE=Release',
                f'-DCMAKE_INSTALL_PREFIX={self.output_dir}'
            ])
        
        print("\nRunning CMake configuration...")
        subprocess.run(cmake_args, check=True)
        
        print("\nBuilding project...")
        if platform.system() == 'Windows':
            build_args = [
                self.msbuild_path,
                str(self.build_dir / 'ALL_BUILD.vcxproj'),
                '/p:Configuration=Release',
                '/p:Platform=x64',
                '/m'
            ]
            subprocess.run(build_args, check=True)
        else:
            subprocess.run(['cmake', '--build', str(self.build_dir), '--config', 'Release'], check=True)
        
        print("\nInstalling to output directory...")
        subprocess.run([
            'cmake',
            '--install', str(self.build_dir),
            '--config', 'Release'
        ], check=True)

    def build_autotools_project(self):
        """Build project using Autotools"""
        print("\nBuilding with Autotools...")
        
        os.chdir(str(self.source_dir))
        
        # Run autogen.sh if it exists
        if (self.source_dir / 'autogen.sh').exists():
            print("\nRunning autogen.sh...")
            subprocess.run(['./autogen.sh'], check=True)
        
        # Run configure if it exists or was generated
        if (self.source_dir / 'configure').exists():
            print("\nRunning configure...")
            subprocess.run([
                './configure',
                f'--prefix={self.output_dir}',
                '--enable-shared'
            ], check=True)
        
        print("\nRunning make...")
        subprocess.run(['make', '-j'], check=True)
        
        print("\nRunning make install...")
        subprocess.run(['make', 'install'], check=True)
        
        os.chdir(str(self.project_root))

    def build_make_project(self):
        """Build project using Make"""
        print("\nBuilding with Make...")
        
        os.chdir(str(self.source_dir))
        
        # Some projects require running ./configure first
        if (self.source_dir / 'configure').exists():
            print("\nRunning configure...")
            subprocess.run([
                './configure',
                f'--prefix={self.output_dir}'
            ], check=True)
        
        print("\nRunning make...")
        subprocess.run(['make', '-j'], check=True)
        
        # Try make install if prefix was set
        try:
            print("\nRunning make install...")
            subprocess.run(['make', 'install'], check=True)
        except subprocess.CalledProcessError:
            print("! Make install failed - copying build artifacts manually")
            # Fallback: Copy all executables and libraries
            self.output_dir.mkdir(parents=True, exist_ok=True)
            for ext in ['', '.exe', '.dll', '.so', '.dylib']:
                for file in self.source_dir.rglob(f'*{ext}'):
                    if file.is_file() and os.access(file, os.X_OK):
                        shutil.copy2(file, self.output_dir)
        
        os.chdir(str(self.project_root))

    def build_project(self):
        """Build the C project using detected build system"""
        self.build_system = self.detect_build_system()
        
        if self.build_system == BuildSystem.CMAKE:
            self.build_cmake_project()
        elif self.build_system == BuildSystem.AUTOTOOLS:
            self.build_autotools_project()
        elif self.build_system == BuildSystem.MAKE:
            self.build_make_project()
        else:
            raise Exception("No supported build system detected")
        
        print(f"\n✓ Project built and installed to: {self.output_dir}")

    def run(self):
        """Run the complete build process"""
        print(f"Starting build process for {self.project_name}...")
        
        # Check dependencies
        missing = self.check_dependencies()
        if missing:
            print("\nMissing required tools. Please install them and try again.")
            sys.exit(1)
        
        try:
            self.clean_directories()
            self.clone_repository()
            self.build_project()
            print("\nBuild process completed successfully!")
            print(f"Output files can be found in: {self.output_dir}")
            
        except Exception as e:
            print(f"\nError during build process: {e}")
            print("\nTroubleshooting tips:")
            print("1. Make sure the repository URL is correct")
            print("2. Verify the project has a supported build system:")
            print("   - CMake (CMakeLists.txt)")
            print("   - Autotools (configure.ac or configure)")
            print("   - Make (Makefile)")
            print("3. Check if you have the necessary permissions")
            print("4. Make sure all dependencies are properly installed")
            if platform.system() == 'Windows':
                print("5. Verify Visual Studio Build Tools are properly installed")
            sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python builder.py <github_url> [branch]")
        print("Example: python builder.py https://github.com/username/project.git main")
        sys.exit(1)
    
    github_url = sys.argv[1]
    branch = sys.argv[2] if len(sys.argv) > 2 else None
    
    builder = CProjectBuilder(github_url, branch)
    builder.run()
