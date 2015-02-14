var gulp        = require('gulp'),
    sass        = require('gulp-sass'),
    minifyCss   = require('gulp-minify-css'),
    jshint      = require('gulp-jshint'),
    uglify      = require('gulp-uglify'),
    concat      = require('gulp-concat'),
    notify      = require('gulp-notify'),
    rename      = require('gulp-rename'),
    del         = require('del'),
    plumber     = require('gulp-plumber'),
    livereload  = require('gulp-livereload'),
    header      = require('gulp-header'),
    process     = require('child_process'),
    //minifyHtml  = require('gulp-minify-html'),
    usemin      = require('gulp-usemin'),
    rev         = require('gulp-rev'),
    mainBowerFiles = require('main-bower-files');


var pkg = require('./package.json');
var banner = ['/**',
  ' * <%= pkg.name %> - <%= pkg.description %>',
  ' * @version v<%= pkg.version %>',
  ' * @author <%= pkg.author %>',
  ' * @link <%= pkg.homepage %>',
  ' * @license <%= pkg.license %>',
  ' */',
  ''].join('\n');


var src = './templates/assets/',
    dest = './app/static/',
    htmlSrc = './templates/',
    htmlDest = './app/templates/';


/* styles */
gulp.task('styles', function () {
    return gulp.src(src+'css/style.scss')
        .pipe(plumber(function (e) {
            console.log('There was an issue compiling Sass');
            console.log(e);
            this.emit('end');
        }))
        .pipe(sass({
            errLogToConsole: true,
            sourceComments : 'normal'
        }))
        .pipe(gulp.dest(dest+'css'))
        .pipe(livereload());
});

gulp.task('copyfiles', function() {
    return gulp.src(src+'css/*.css')
        .pipe(gulp.dest(dest+'/css'));
});


gulp.task('bower', function (){
    return gulp.src(mainBowerFiles(), {base: './bower_components/'})
        .pipe(gulp.dest('./templates/assets/vendor/'));
});


gulp.task('styles-dist', function (){
    return gulp.src(src+'css/style.scss')
        .pipe(plumber(function () {
            console.log('There was an issue compiling Sass');
            this.emit('end');
        }))
        .pipe(sass())
        .pipe(gulp.dest(dest+'css'))
        .pipe(rename({ suffix: '.min' }))
        .pipe(minifyCss())
        .pipe(header(banner, { pkg : pkg } ))
        .pipe(gulp.dest(dest+'css'));
});


/* scripts */
gulp.task('scripts', function(){
    return gulp.src(src+'js/**//*.js')
        .pipe(plumber(function () {
            console.log('There was an issue processing JS.');
            this.emit('end');
        }))
        .pipe(jshint('.jshintrc'))
        .pipe(jshint.reporter('default'))
        .pipe(concat('all.js'))
        .pipe(gulp.dest(dest+'js'))
        .pipe(livereload());
});

gulp.task('scripts-dist', function(){
    return gulp.src(src+'js/**/*.js')
        .pipe(plumber(function () {
            console.log('There was an issue processing JS.');
            this.emit('end');
        }))
        .pipe(jshint('.jshintrc'))
        .pipe(jshint.reporter('default'))
        .pipe(concat('all.js'))
        .pipe(gulp.dest(dest+'js'))
        .pipe(rename({ suffix: '.min' }))
        .pipe(uglify({mangle: true}))
        .pipe(header(banner, { pkg : pkg } ))
        .pipe(gulp.dest(dest+'js'));
});


gulp.task('usemin', ['bower'], function(){
    return gulp.src(['./templates/base1.html'])
        .pipe(usemin({
            css: [minifyCss(), 'concat'],
            //html: [minifyHtml({empty: true})],
            js: [uglify(), 'concat']
        }))
        .pipe(gulp.dest('./app/templates/'));
});


/* clean */
gulp.task('clean', function(cb){
    return del([dest, 'templates/assets/vendor/'], cb);
});
gulp.task('clean-dist', function(cb){
    return del([dest+'css/**/*.min.css', dest+'js/**/*.min.js'], cb);
});


gulp.task('flask', function(){
    var spawn = process.spawn;
    console.info('Starting flask server');
    var PIPE = {stdio: 'inherit'};
    spawn('python', ['manage.py','runserver','-h','127.0.0.1'], PIPE);
});


gulp.task('init', function(){
    var spawn = process.spawn;
    console.info('python manage.py db upgarade');
    var PIPE = {stdio: 'inherit'};
    spawn('python', ['manage.py','db','upgrade'], PIPE);
});


gulp.task('watch', function() { 
    // Watch image files
    //gulp.watch('src/images/**//*', ['images']);
 
    // Create LiveReload server
    livereload.listen({
        port: 35729
    });
    console.info('Livereload on PORT '+livereload.options.port);

    // Watch .scss files
    gulp.watch(src+'css/**/*.scss', ['styles']);
 
    // Watch .js files
    gulp.watch(src+'js/**/*.js', ['scripts']);

    // Watch static files
    gulp.watch([src+'css/**/*.css', src+'js/**/*.js'], ['copyfiles']);

    // Watch template changes
    gulp.watch(htmlSrc + 'base1.html', ['usemin']);
    gulp.watch(htmlDest + '**/*.html', livereload.reload);
});


gulp.task('dist', ['clean'], function() {
    gulp.start('styles-dist', 'scripts-dist');
});

gulp.task('default', ['clean'], function() {
    gulp.start('styles', 'copyfiles', 'scripts', 'usemin');
});

gulp.task('serve',['default'], function(){
    gulp.start('flask', 'watch');
});
