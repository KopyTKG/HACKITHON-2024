const lat = [48.55, 51.05]
const lon = [12.09, 18.86]

function generateData() {
 const data = []
 for (let i = 0; i < 6000; i++) {
  data.push({
   coordinates: [
    lon[0] + Math.random() * (lon[1] - lon[0]),
    lat[0] + Math.random() * (lat[1] - lat[0]),
   ],
   nazev: `Dokument ${i}`,
  })
 }
 return data
}

export function GET(req: NextRequest) {
 return new Response(JSON.stringify(generateData()))
}
