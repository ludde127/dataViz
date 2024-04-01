import * as esbuild from "esbuild";
import stylePlugin from "esbuild-style-plugin";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";
import chokidar from "chokidar";

const ctx = await esbuild.context({
    entryPoints: ["src/*.ts"],
    outdir: "../static/compiled/",
    bundle: true,
    minify: true,
    treeShaking: true,
    plugins: [stylePlugin({
        postcss: {
            plugins: [tailwindcss, autoprefixer]
        }
    })],
});

const watcher = chokidar.watch(["../**/*.html", "src/**/*.{ts,css}"], {
    persistent: true
});

watcher.on("change", async path => {
    console.log(`Detected changed in: ${path}`);
    await ctx.rebuild();
});

console.log("Watching...");