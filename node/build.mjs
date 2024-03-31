import * as esbuild from "esbuild";
import stylePlugin from "esbuild-style-plugin";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";

const ctx = await esbuild.context({
    entryPoints: ["src/*.ts"],
    outdir: "../static/compiled/",
    bundle: true,
    minify: true,
    treeShaking: true,
    plugins: [
        stylePlugin({
            postcss: {
                plugins: [tailwindcss, autoprefixer]
            }
        })
    ],
});

await ctx.watch();
console.log("Watching...");