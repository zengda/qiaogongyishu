const ci = require('miniprogram-ci')

function parseArgs() {
  const args = process.argv.slice(2)
  const result = { _: [] }
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].replace(/^--/, '')
      const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true
      result[key] = value
    } else {
      result._.push(args[i])
    }
  }
  return result
}

async function main() {
  const args = parseArgs()
  const command = args._[0]

  const projectConfig = {
    appid: args.appid,
    type: args.type || 'miniProgram',
    projectPath: args['project-path'],
    privateKeyPath: args['private-key-path'],
    ignores: ['node_modules/**/*']
  }

  const project = new ci.Project(projectConfig)

  if (command === 'upload') {
    const version = args.version
    const desc = args.desc || ''
    const robot = parseInt(args.robot) || 1

    const uploadResult = await ci.upload({
      project,
      version,
      desc,
      robot,
      setting: {
        es6: true,
        es7: true,
        minifyJS: true,
        minifyWXML: true,
        minifyWXSS: true,
        minify: true,
        codeProtect: false,
        autoPrefixWXSS: true
      },
      onProgressUpdate: (info) => {
        if (info && info.status !== 'done') {
          console.log(JSON.stringify(info))
        }
      }
    })

    console.log(JSON.stringify({ success: true, version, desc }))
    return
  }

  if (command === 'preview') {
    const desc = args.desc || '从管理后台预览'
    const pagePath = args['page-path'] || 'pages/index/index'
    const searchQuery = args['search-query'] || ''
    const robot = parseInt(args.robot) || 1
    const qrcodeFormat = args['qrcode-format'] || 'image'
    const qrcodeOutputDest = args['qrcode-output']

    const previewResult = await ci.preview({
      project,
      desc,
      robot,
      setting: {
        es6: true,
        es7: true,
        minifyJS: true,
        minifyWXML: true,
        minifyWXSS: true,
        autoPrefixWXSS: true
      },
      qrcodeFormat,
      qrcodeOutputDest,
      pagePath,
      searchQuery,
      scene: 1011,
      onProgressUpdate: (info) => {
        if (info && info.status !== 'done') {
          console.log(JSON.stringify(info))
        }
      }
    })

    console.log(JSON.stringify({ success: true }))
    return
  }

  console.error('Unknown command: ' + command)
  process.exit(1)
}

main().catch((err) => {
  console.error(err.message || err)
  process.exit(1)
})
