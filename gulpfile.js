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

var src = {
    root: './frontend/',
    html: './frontend/**//*.html',
    scss: './frontend/static/sass/',
    js: './frontend/static/js/',
    css: './frontend/static/css/',
    img: './frontend/static/img/'
};

var dest = {
    root: './templates/',
    static: './templates/static/',
    css: './templates/static/css/',
    js: './templates/static/js/'
};


/* styles */
gulp.task('styles', function () {
    return gulp.src(src.scss+'style.scss')
        .pipe(plumber(function (e) {
            console.log('There was an issue compiling Sass');
            console.log(e);
            this.emit('end');
        }))
        .pipe(sass({
            errLogToConsole: true,
            sourceComments : 'normal'
        }))
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(src.css))
        .pipe(livereload());
});


/*gulp.task('styles-dist', function (){
    return gulp.src(src+'css/style.scss')
        .pipe(plumber(function () {
            console.log('There was an issue compiling Sass');
            this.emit('end');
        }))
        .pipe(sass())
        .pipe(gulp.dest(dest+'css'))
        //.pipe(rename({ suffix: '.min' }))
        .pipe(minifyCss())
        .pipe(header(banner, { pkg : pkg } ))
        .pipe(gulp.dest(dest+'css'));
});*/


/* scripts */
gulp.task('scripts', function(){
    return gulp.src(src.js+"*.js")
        .pipe(plumber(function () {
            console.log('There was an issue processing JS.');
            this.emit('end');
        }))
        .pipe(jshint('.jshintrc'))
        .pipe(jshint.reporter('default'))
        .pipe(concat('script.js'))
        .pipe(rename({ suffix: '.min' }))
        .pipe(gulp.dest(src.js))
        .pipe(livereload());
});

/*gulp.task('scripts-dist', function(){
    return gulp.src(src.js+'*.js')
        .pipe(plumber(function () {
            console.log('There was an issue processing JS.');
            this.emit('end');
        }))
        .pipe(jshint('.jshintrc'))
        .pipe(jshint.reporter('default'))
        .pipe(concat('all.js'))
        .pipe(gulp.dest(dest+'js'))
        //.pipe(rename({ suffix: '.min' }))
        .pipe(uglify({mangle: true}))
        .pipe(header(banner, { pkg : pkg } ))
        .pipe(gulp.dest(dest+'js'));
});*/


gulp.task('copyfiles', function() {
    return gulp.src(src.img)
        .pipe(gulp.dest(dest.static));
});


gulp.task('usemin', ['styles', 'scripts', 'copyfiles'], function(){
    return gulp.src(src.html)
        .pipe(usemin({
            cssv: ['concat'],
            css: ['concat'],
            //html: [minifyHtml({empty: true})],
            js: [jshint('.jshintrc')],
            jsv: ['concat']
        }))
        .pipe(gulp.dest(dest.root))
        .pipe(livereload());
});


/* clean */
gulp.task('clean', function(cb){
    return del([dest.root, src.css+"*.min.css", src.js+"*.min.js"], function (err, paths) {
        console.log('Deleted files/folders:\n', paths.join('\n'));
        cb();
    });
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
    gulp.watch(src.sass+'*.scss', ['styles']);
 
    // Watch .js files
    gulp.watch(src.js+'*.js', ['scripts']);

    // Watch static files
    //gulp.watch(src+'css/**/*.css', ['copyfiles-css']);
    //gulp.watch(src+'css/**/*.v.js', ['copyfiles-js']);

    // Watch template changes
    //gulp.watch(htmlSrc + 'base1.html', ['usemin']);
    //gulp.watch(htmlDest + '**/*.html', livereload.reload);
});


gulp.task('dist', ['clean'], function() {
    gulp.start('styles-dist', 'copyfiles-css', 'copyfiles-js', 'scripts-dist', 'usemin');
});

gulp.task('default', ['clean'], function() {
    gulp.start('styles', 'copyfiles-css', 'copyfiles-js', 'scripts', 'usemin');
});

gulp.task('serve',['default'], function(){
    gulp.start('flask', 'watch');
});
