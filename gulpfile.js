var gulp = require('gulp'),
    sass = require('gulp-sass'),
    minifyCss = require('gulp-minify-css'),
    jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat'),
    notify = require('gulp-notify'),
    rename = require('gulp-rename'),
    del = require('del'),
    header = require('gulp-header');


var pkg = require('./package.json');
var banner = ['/**',
  ' * <%= pkg.name %> - <%= pkg.description %>',
  ' * @version v<%= pkg.version %>',
  ' * @author <%= pkg.author %>',
  ' * @link <%= pkg.homepage %>',
  ' * @license <%= pkg.license %>',
  ' */',
  ''].join('\n');


var src = './static/',
    dest = './app/static/';

gulp.task('styles', function (){
    return gulp.src(src+'css/main.scss')
        .pipe(sass())
        .pipe(gulp.dest(dest+'css'));
});

gulp.task('styles-dist', function (){
    return gulp.src(src+'css/main.scss')
        .pipe(sass())
        .pipe(gulp.dest(dest+'css'))
        .pipe(rename({ suffix: '.min' }))
        .pipe(minifyCss())
        .pipe(header(banner, { pkg : pkg } ))
        .pipe(gulp.dest(dest+'css'));
});


gulp.task('scripts', function(){
    return gulp.src(src+'js/**/*.js')
        .pipe(jshint('.jshintrc'))
        .pipe(jshint.reporter('default'))
        .pipe(concat('all.js'))
        .pipe(gulp.dest(dest+'js'));
});

gulp.task('scripts-dist', function(){
    return gulp.src(src+'js/*.js')
        .pipe(jshint('.jshintrc'))
        .pipe(jshint.reporter('default'))
        .pipe(concat('all.js'))
        .pipe(gulp.dest(dest+'js'))
        .pipe(rename({ suffix: '.min' }))
        .pipe(uglify({mangle: true}))
        .pipe(header(banner, { pkg : pkg } ))
        .pipe(gulp.dest(dest+'js'));
});

gulp.task('clean', function(cb){
    del([dest+'css', dest+'js'], cb);
});

gulp.task('dist', ['clean'], function() {
    gulp.start('styles-dist', 'scripts-dist');
});

gulp.task('default', ['clean'], function() {
    gulp.start('styles', 'scripts');
});

/*
var gulp = require('gulp'),
    sass = require('gulp-ruby-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    minifycss = require('gulp-minify-css'),
    jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    notify = require('gulp-notify'),
    cache = require('gulp-cache'),
    livereload = require('gulp-livereload'),
    del = require('del');
 
// Styles
gulp.task('styles', function() {
  return gulp.src('src/styles/main.scss')
    .pipe(sass({ style: 'expanded', }))
    .pipe(autoprefixer('last 2 version', 'safari 5', 'ie 8', 'ie 9', 'opera 12.1', 'ios 6', 'android 4'))
    .pipe(gulp.dest('dist/styles'))
    .pipe(rename({ suffix: '.min' }))
    .pipe(minifycss())
    .pipe(gulp.dest('dist/styles'))
    .pipe(notify({ message: 'Styles task complete' }));
});
 
// Scripts
gulp.task('scripts', function() {
  return gulp.src('src/scripts/**//*.js')
    .pipe(jshint('.jshintrc'))
    .pipe(jshint.reporter('default'))
    .pipe(concat('main.js'))
    .pipe(gulp.dest('dist/scripts'))
    .pipe(rename({ suffix: '.min' }))
    .pipe(uglify())
    .pipe(gulp.dest('dist/scripts'))
    .pipe(notify({ message: 'Scripts task complete' }));
});
 
// Images
gulp.task('images', function() {
  return gulp.src('src/images/**//*')
    .pipe(cache(imagemin({ optimizationLevel: 3, progressive: true, interlaced: true })))
    .pipe(gulp.dest('dist/images'))
    .pipe(notify({ message: 'Images task complete' }));
});
 
// Clean
gulp.task('clean', function(cb) {
    del(['dist/assets/css', 'dist/assets/js', 'dist/assets/img'], cb)
});
 
// Default task
gulp.task('default', ['clean'], function() {
    gulp.start('styles', 'scripts', 'images');
});
 
// Watch
gulp.task('watch', function() {
 
  // Watch .scss files
  gulp.watch('src/styles/**//*.scss', ['styles']);
 
  // Watch .js files
  gulp.watch('src/scripts/**//*.js', ['scripts']);
 
  // Watch image files
  gulp.watch('src/images/**//*', ['images']);
 
  // Create LiveReload server
  livereload.listen();
 
  // Watch any files in dist/, reload on change
  gulp.watch(['dist/**']).on('change', livereload.changed);
 
});*/
