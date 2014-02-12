module.exports = (grunt) ->
  grunt.loadNpmTasks 'grunt-contrib-connect'
  grunt.loadNpmTasks 'grunt-contrib-less'
  grunt.loadNpmTasks 'grunt-autoprefixer'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-copy'
  grunt.loadNpmTasks 'grunt-contrib-coffee'

  grunt.initConfig(
    connect:
      dist:
        options:
          keepalive: true
          port: 9871
          base: 'dist/'
      dev:
        options:
          port: 9871
          base: 'dist/'
    less:
      dist:
        files: [
          expand: true
          cwd: 'src/less/'
          src: ['**/*.less', '!**/_*.less']
          dest: '.tmp/css/'
          ext: '.css'
        ]
    autoprefixer:
      dist:
        options:
          browsers: ['last 2 versions']
        files:[
          expand: true
          cwd: '.tmp/css/'
          src: ['**/*.css']
          dest: 'dist/css/'
          ext: '.css'
        ]
    watch:
      asset_css:
        files: ['src/less/**/*']
        tasks: ['css']
        options : { nospawn : true }
      asset_js:
        files: ['src/coffee/**/*']
        tasks: ['coffee']
        options : { nospawn : true }
      asset_index:
        files: ['src/index.html']
        tasks: ['copy:index']
    copy:
      index:
        files: [
          expand: true
          cwd: 'src/'
          src: ['index.html']
          dest: 'dist/'
        ]
      vendor:
        files: [
          expand: true
          cwd: 'vendor/'
          src: ['**/*.js']
          dest: 'dist/js/'
        ]
    coffee:
      compile:
        files: [
          expand: true
          cwd: 'src/coffee/'
          src: ['**/*.coffee']
          dest: 'dist/js/'
          ext: '.js'
        ]
  )

  grunt.registerTask 'css', [
    'less:dist'
    'autoprefixer:dist'
  ]
  grunt.registerTask 'server', [
    'default'
    'connect:dist'
  ]
  grunt.registerTask 'dev', [
    'default'
    'connect:dev'
    'watch'
  ]
  grunt.registerTask 'default', [
    'css'
    'copy'
    'coffee'
  ]

