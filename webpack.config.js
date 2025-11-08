const path = require('path');
const { styles } = require('@ckeditor/ckeditor5-dev-utils');
const { merge } = require('webpack-merge');

const defaultConfig = {
  resolve: {
    extensions: ['.ts', '.tsx', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: 'ts-loader',
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: styles.getPostCssConfig({
                themeImporter: {
                  themePath: require.resolve('@ckeditor/ckeditor5-theme-lark'),
                },
                minify: true,
              }),
            },
          },
        ],
      },
      {
        test: /\.svg$/,
        use: [
          {
            loader: 'raw-loader',
          },
        ],
        include: /ckeditor5-[^/\\]+[/\\]theme[/\\]icons/,
      },
      {
        test: /\.svg$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'icons/',
              publicPath: 'icons/',
              esModule: false,
            },
          },
        ],
        exclude: /ckeditor5-[^/\\]+[/\\]theme[/\\]icons/,
      },
    ],
  },
};

const baseConfig = {
  entry: {
    main: './src/base.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/base.js',
  },
};

const userConfig = {
  entry: {
    main: './src/user.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/user.js',
  },
};

const ckeditorConfig = {
  entry: {
    main: './src/ckeditor.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/ckeditor.js',
  },
};

const transactionsConfig = {
  entry: {
    main: './src/transactions.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/transactions.js',
  },
};

const configs = [
  baseConfig,
  userConfig,
  ckeditorConfig,
  transactionsConfig,
].map(conf =>
  merge(defaultConfig, conf),
);

module.exports = configs;
