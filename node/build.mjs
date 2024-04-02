import * as esbuild from "esbuild";
import {analyzeMetafile} from "esbuild";
import stylePlugin from "esbuild-style-plugin";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";
import chokidar from "chokidar";
import cssnanoPlugin from "cssnano";

const ctx = await esbuild.context({
    entryPoints: ["src/*.ts"],
    outdir: "../static/compiled/",
    bundle: true,
    minify: true,
    sourcemap: true,
    treeShaking: true,
    metafile: true,
    plugins: [stylePlugin({
        postcss: {
            plugins: [tailwindcss, autoprefixer, cssnanoPlugin]
        }
    })],
});

const watcher = chokidar.watch(["../**/*.html", "src/**/*.{ts,css}"], {
    persistent: true
});

const doBuild = async () => {
    try {
        const build = await ctx.rebuild();
        console.log(await analyzeMetafile(build.metafile, {
            color: true, verbose: false
        }));
    } catch (e) {
        console.error(e);
    }
}

watcher.on("change", async path => {
    console.log(`Detected changed in: ${path}`);
    await doBuild();
});

console.log("Watching...");
await doBuild();
