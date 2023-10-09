## Set up develop enviroment in Ubuntu 20.04

1. Install NVM - Node Version Manager manage Node versions
   - Run the nvm installer
     ```bash
     curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
     ```
   - Update your profile configuration
     ```bash
     export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
     ```
   - Reload the shell configuration
     ```bash
     source ~/.bashrc
     ```
     ```bash
     nvm -v
     ```
2. Install node 18
   ```bash
   nvm install 18
   ```
   ```bash
   nvm use 18
   ```
3. Install library

   ```bash
   npm install
   ```

4. Run the development server:

   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

5. Run the production server:

   ```bash
   npm run build

   npm start
   ```
