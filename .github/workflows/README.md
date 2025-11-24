# GitHub Actions Workflows

This directory contains GitHub Actions workflows for automated builds and releases.

## Available Workflows

### 1. `build-windows.yml`
**Purpose**: Build Windows executable on every push/PR

**Triggers**:
- Push to `main` or `master` branch
- Pull requests
- Tags starting with `v*`
- Manual workflow dispatch

**Output**: 
- Windows executable artifact: `CTF_Tool_Selector-Windows`
- Creates GitHub release on tag push

### 2. `build-all-platforms.yml`
**Purpose**: Build executables for Windows, Linux, and macOS

**Triggers**:
- Push to `main` or `master` branch
- Tags starting with `v*`
- Manual workflow dispatch

**Output**:
- Windows executable: `CTF_Tool_Selector-Windows`
- Linux executable: `CTF_Tool_Selector-Linux`
- macOS executable: `CTF_Tool_Selector-macOS`
- Creates GitHub release with all platforms on tag push

## How to Use

### Download Latest Build

1. Go to the [Actions](https://github.com/psworld143/ctf_tools/actions) tab
2. Click on the latest successful workflow run
3. Scroll down to "Artifacts"
4. Download the executable for your platform

### Create a Release

1. Create and push a tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. GitHub Actions will automatically:
   - Build executables for all platforms
   - Create a GitHub release
   - Attach all executables to the release

### Manual Trigger

1. Go to the [Actions](https://github.com/psworld143/ctf_tools/actions) tab
2. Select the workflow you want to run
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## Workflow Details

### Build Process

1. **Checkout code**: Gets the latest code from repository
2. **Setup Python**: Installs Python 3.11
3. **Install dependencies**: Installs requirements.txt (including PyInstaller)
4. **Build executable**: Runs PyInstaller with optimized settings
5. **Upload artifact**: Makes executable available for download
6. **Create release** (on tags): Creates GitHub release with executables

### Build Configuration

- **Python version**: 3.11
- **Architecture**: x64
- **Build type**: One-file executable
- **Bundled files**: `ai_providers.sql`
- **Hidden imports**: All required modules

## Troubleshooting

### Build Fails

- Check the Actions tab for error messages
- Ensure `requirements.txt` includes all dependencies
- Verify `ai_providers.sql` exists in the repository

### Artifact Not Available

- Artifacts expire after 30 days (free tier)
- Re-run the workflow to generate new artifacts
- Use releases for permanent downloads

### Release Not Created

- Ensure tag starts with `v` (e.g., `v1.0.0`)
- Check that workflow has permission to create releases
- Verify `GITHUB_TOKEN` is available (automatically provided)

## Customization

To modify build settings, edit the workflow files:
- Change Python version in `setup-python` step
- Modify PyInstaller flags
- Add additional build steps
- Change artifact retention period

