/* eslint-disable */

import {resolve} from 'path';

import * as AutoPrefixer from 'autoprefixer';
import * as CopyPlugin from 'copy-webpack-plugin';
import * as MiniCssExtractPlugin from 'mini-css-extract-plugin';
import * as StylelintPlugin from 'stylelint-webpack-plugin';

// @ts-ignore
import * as AssetsMapWriterPlugin from './cosmogo/assets/assets-map-writer-plugin';

const extractCss = new MiniCssExtractPlugin({
    filename: 'css/[name].[chunkhash].css',  /* the path is relative to the output path */
});

const publicPath = '/static/';

const plugins = [
    extractCss,
    // @ts-ignore
    new StylelintPlugin({
        context: resolve(__dirname, 'swp', 'assets', 'styles'),
    }),
    new CopyPlugin({
        patterns: [
            {from: 'swp/assets/i18n', to: 'i18n/[name].[contenthash].[ext]'},
        ],
    }),
    new AssetsMapWriterPlugin('../assets/assets.map.json'),
];

const uncommon = [
    'sentry',
];

const config = {
    entry: {
        /* main */
        swp: 'swp/index.js',

        /* uncommon */
        // sentry: 'swp/sentry.js',
    },
    resolve: {
        alias: {
            styles: resolve(__dirname, 'swp', 'assets', 'styles'),
            swp: resolve(__dirname, 'swp', 'assets', 'scripts'),
            utils: resolve(__dirname, 'swp', 'assets', 'scripts', 'utils'),
            components: resolve(__dirname, 'swp', 'assets', 'scripts', 'components'),
            hooks: resolve(__dirname, 'swp', 'assets', 'scripts', 'hooks'),
        },
    },
    output: {
        path: resolve(__dirname, 'swp', 'static'),
        filename: 'js/[name].[chunkhash].js',
        hashFunction: 'sha256',
        hashDigestLength: 16,
        hashDigest: 'hex',
        publicPath,
    },
    optimization: {
        splitChunks: {
            chunks: ({name}) => uncommon.indexOf(name) < 0,
            minChunks: 2,
            maxAsyncRequests: 1,
            maxInitialRequests: 2,
            name: 'common',
        },
    },
    devtool: 'source-map',
    module: {
        rules: [
            {
                test: /\.s?[ca]ss$/,
                use: [
                    {loader: MiniCssExtractPlugin.loader},
                    {loader: 'css-loader', options: {sourceMap: true, url: true}},
                    {loader: 'postcss-loader', options: {postcssOptions: {plugins: [AutoPrefixer()]}, sourceMap: true}},
                    {loader: 'sass-loader', options: {sourceMap: true}},
                ],
            },
            {
                enforce: 'pre',
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'eslint-loader',
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            ['@babel/preset-react', {'runtime': 'automatic'}],
                            ['@babel/preset-env', {
                                modules: false,
                                useBuiltIns: 'usage',
                                corejs: 3,
                                loose: true,
                                targets: {
                                    ie: 11,
                                    safari: 7,
                                },
                            }],
                        ],
                        plugins: [
                            '@babel/proposal-object-rest-spread',
                        ],
                    },
                },
            },
            {
                test: /\.(ttf|eot|woff2?)$/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: 'fonts/[name].[sha256:hash:base62:16].[ext]',
                        publicPath,
                    },
                },
            },
            {
                test: /\.svg$/,
                exclude: /node_modules/,
                loader: 'svg-react-loader',
            },
            {
                test: /\.(jpe?g|png|gif)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'file-loader',
                    options: {
                        name: 'images/[name].[sha256:hash:base62:16].[ext]',
                        publicPath,
                    },
                },
            },
        ],
    },
    plugins,
};

module.exports = config;