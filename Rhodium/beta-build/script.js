var data_nodes
		var data_links
		let highlight = []
		let highlight_link = []

		async function load_data(){

			data = await fetch("../data/node.json")
				.then(response => {
					return response.json();
				})

			data2 = await fetch("../data/link.json")
					.then(response => {
						return response.json();
					})

			return (data,data2)
		}
		console.log('🟡 Engaging Ressources... ')
		var data, data2 = load_data().then( help => {
			setTimeout(() => {  console.log("Ressources Loaded 🌵"); }, 1000)
			console.log('🟢 Ressources Online')

			const gData = {
					nodes: data,
					links: data2
				};

					console.log('🟡 Starting Graph\'s Protocols... 📈')
					const Graph = ForceGraph3D()
					(document.getElementById('3d-graph'))
						.nodeOpacity(1)
						.linkOpacity(1)
						.nodeAutoColorBy('type')
						//.nodeColor(d => d.status=='positive' ? '#ff5555ff' : d.status=='close to' ? '#ffaa55ff' : '#ffffffaa')
						.linkColor(d => d.type=='Cas Contact' ? '#ffaa55ff' : d.type=='Positif' ? '#ff5555ff' : '#ffffffaa')
						.linkWidth(d => d.type=='Cas Contact' ? 1 : d.type=='Positif' ? 1 : 0.1)
						.nodeVal(d => d.type==d.name ? 10 : 1)
						.graphData(gData)
						.nodeThreeObject(({ hasCustomImage,img }) => {
							if(hasCustomImage == 'true'){
								const imgTexture = new THREE.TextureLoader().load(`../imgs/${img}.png`)
								const material = new THREE.SpriteMaterial({ map: imgTexture });
								const sprite = new THREE.Sprite(material);
								sprite.scale.set(12, 12);
							return sprite;
							}
						});
					console.log('🟢 Graph Is On The Field !')
		})
