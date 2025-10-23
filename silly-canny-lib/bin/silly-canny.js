#!/usr/bin/env node
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const args = process.argv.slice(2)
const cmd = args[0]
const comp = args[1]

if (cmd !== 'add' || !comp) {
  console.error('Usage: silly-canny add <ComponentName>')
  process.exit(1)
}

const src = path.resolve(__dirname, '../components/ui', `${comp}.vue`)
const destDir = path.resolve(process.cwd(), 'src/components/ui')
const dest = path.join(destDir, `${comp}.vue`)

if (!fs.existsSync(src)) {
  console.error(`❌ Component "${comp}" not found.`)
  process.exit(1)
}

fs.mkdirSync(destDir, { recursive: true })
fs.copyFileSync(src, dest)
console.log(`✅ Added ${comp} to src/components/ui/`)
