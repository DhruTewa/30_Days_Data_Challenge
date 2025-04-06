// main.js
document.addEventListener('DOMContentLoaded', function() {
    const data = [30, 86, 168, 234, 200, 100, 300];

    const width = 500;
    const height = 300;
    const barPadding = 5;

    const svg = d3.select('body')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    const barWidth = width / data.length;

    const bars = svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('x', (d, i) => i * barWidth)
        .attr('y', d => height - d)
        .attr('width', barWidth - barPadding)
        .attr('height', d => d)
        .attr('fill', 'teal')
        .attr('opacity', 0)
        .transition()
        .duration(1000)
        .attr('opacity', 1);

    svg.selectAll('text')
        .data(data)
        .enter()
        .append('text')
        .text(d => d)
        .attr('x', (d, i) => i * barWidth + (barWidth - barPadding) / 2)
        .attr('y', d => height - d - 5)
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .attr('opacity', 0)
        .transition()
        .duration(1000)
        .attr('opacity', 1);
});