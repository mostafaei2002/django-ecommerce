"use strict";

const path = require("path");
const autoprefixer = require("autoprefixer");
const miniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    mode: "development",
    entry: "./frontend/js/main.js",
    output: {
        filename: "main.js",
        path: path.resolve(__dirname, "../backend/static"),
    },
    plugins: [new miniCssExtractPlugin()],
    module: {
        rules: [
            {
                test: /\.(scss)$/,
                use: [
                    {
                        // Extract css into a separate file
                        loader: miniCssExtractPlugin.loader,
                    },
                    {
                        // Interprets `@import` and `url()` like `import/require()` and will resolve them
                        loader: "css-loader",
                    },
                    {
                        // Loader for webpack to process CSS with PostCSS
                        loader: "postcss-loader",
                        options: {
                            postcssOptions: {
                                plugins: [autoprefixer],
                            },
                        },
                    },
                    {
                        // Loads a SASS/SCSS file and compiles it to CSS
                        loader: "sass-loader",
                    },
                ],
            },
        ],
    },
};
