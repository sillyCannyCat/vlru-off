import vue from '@vitejs/plugin-vue'
import path from 'path'
import { defineConfig } from 'vite'

export default defineConfig(({ command }) => ({
  plugins: [vue()],
  build:
    command === 'build'
      ? {
          lib: {
            entry: path.resolve(__dirname, 'src/lib.js'),
            name: 'SillyCannyLib',
            fileName: (format) => `silly-canny-lib.${format}.js`,
          },
          rollupOptions: {
            external: ['vue'],
            output: {
              globals: {
                vue: 'Vue',
              },
            },
          },
        }
      : {},
}))
