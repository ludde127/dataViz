import * as esbuild from "esbuild";
import stylePlugin from "esbuild-style-plugin";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";
import gzipPlugin from "@luncheon/esbuild-plugin-gzip";

const ctx = await esbuild.context({
    entryPoints: ["src/*.ts"],
    outdir: "../static/compiled/",
    bundle: true,
    minify: true,
    treeShaking: true,
    write: false,
    plugins: [
        stylePlugin({
            postcss: {
                plugins: [tailwindcss, autoprefixer]
            }
        }),
        gzipPlugin({
            uncompressed: false,
            gzip: false,
            brotli: true,
        })
    ],
});

await ctx.watch();
console.log("Watching...");