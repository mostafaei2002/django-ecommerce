"use strict";

const path = require("path");
const autoprefixer = require("autoprefixer");
const miniCssExtractPlugin = require("mini-css-extract-plugin");
const glob = require("glob");

const getAllEntryPoints = () => {
    const entryPoints = {};

    const jsFiles = glob.sync(path.join(__dirname, "js/*.js"));
    jsFiles.forEach((file) => {
        const entryName = path.basename(file, path.extname(file));
        entryPoints[entryName] = file;
    });

    console.log(entryPoints);

    return entryPoints;
};

module.exports = {
    mode: "development",
    entry: getAllEntryPoints(),
    output: {
        filename: "[name].js",
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
