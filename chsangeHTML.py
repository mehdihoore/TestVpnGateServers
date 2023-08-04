
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      /* Add some basic CSS styles to make the table responsive */
      table {
        width: 100%;
        border-collapse: collapse;
      }

      th, td {
        border: 1px solid #dddddd;
        /* Light gray border between cells */
        padding: 8px;
        text-align: left;
        /* Align table cell text to the left */
        min-width: 1px;
        /* Set minimum width to 1px */
        max-width: 100%;
        /* Set maximum width to 100% */
        overflow: hidden;
        /* Hide any overflowing content */
        white-space: nowrap;
        /* Prevent text from wrapping */
      }

      /* Apply styles for the table header */
      thead th {
        background-color: #f2f2f2;
        /* Light gray background color */
        color: #333333;
        /* Dark gray text color */
        font-weight: bold;
        /* Bold font weight for header text */
        text-align: center;
        /* Center header text */
      }

      /* Apply custom font to the table */
      table {
        font-family: Tahoma, sans-serif;
      }

      /* Make the table responsive */
      @media screen and (max-width: 200px) {

        /* For smaller screens, reduce font size and wrap table cells */
        th, td {
          font-size: 14px;
          white-space: wrap;
        }
      }
    </style>
</head>
<body>
    <select id="filterCountry" onchange="filterTable()">
        <option value="All Countries">All Countries</option><option value="Germany">Germany</option><option value="Japan">Japan</option><option value="Korea Republic of">Korea Republic of</option><option value="Russian Federation">Russian Federation</option><option value="Thailand">Thailand</option><option value="United States">United States</option>
    </select>
    
<script>
function filterTable() {
  const inputCountry = document.getElementById('filterCountry').value.toLowerCase();
  const rows = document.querySelectorAll('tbody tr');

  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    const country = row.children[0].innerText.toLowerCase();

    if (inputCountry === 'all countries' || country.includes(inputCountry)) {
      row.style.display = 'table-row';
    } else {
      row.style.display = 'none';
    }
  }
}
</script>

    <table border="1" class="dataframe dataframe">
  <thead>
<tr><th>Country</th><th>Ping Time</th><th>SSTP Link</th></tr>

    <tr style="text-align: right;">
      <th>country</th>
      <th>Ping Time</th>
      <th>sstp</th>
      <th>sstp_link</th>
    </tr>
  </thead>
  <tbody>

    <tr>
      <td>United States</td>
      <td>1</td>
      <td>vpn906128495.opengw.net</td>
      <td><a href="vpn906128495.opengw.net">vpn906128495.opengw.net</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>2</td>
      <td>vpn360221840.opengw.net:1402</td>
      <td><a href="vpn360221840.opengw.net:1402">vpn360221840.opengw.net:1402</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>2</td>
      <td>vpn849511280.opengw.net:1345</td>
      <td><a href="vpn849511280.opengw.net:1345">vpn849511280.opengw.net:1345</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>2</td>
      <td>vpn435394266.opengw.net:1495</td>
      <td><a href="vpn435394266.opengw.net:1495">vpn435394266.opengw.net:1495</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>3</td>
      <td>vpn350704800.opengw.net:1309</td>
      <td><a href="vpn350704800.opengw.net:1309">vpn350704800.opengw.net:1309</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>3</td>
      <td>vpn447177167.opengw.net:1575</td>
      <td><a href="vpn447177167.opengw.net:1575">vpn447177167.opengw.net:1575</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>3</td>
      <td>vpn442207144.opengw.net:1960</td>
      <td><a href="vpn442207144.opengw.net:1960">vpn442207144.opengw.net:1960</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>3</td>
      <td>vpn680583464.opengw.net:1958</td>
      <td><a href="vpn680583464.opengw.net:1958">vpn680583464.opengw.net:1958</a></td>
    </tr>
    <tr>
      <td>United States</td>
      <td>4</td>
      <td>vpn431396938.opengw.net</td>
      <td><a href="vpn431396938.opengw.net">vpn431396938.opengw.net</a></td>
    </tr>
    <tr>
      <td>United States</td>
      <td>4</td>
      <td>vpn719329406.opengw.net</td>
      <td><a href="vpn719329406.opengw.net">vpn719329406.opengw.net</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>4</td>
      <td>vpn501762624.opengw.net:1577</td>
      <td><a href="vpn501762624.opengw.net:1577">vpn501762624.opengw.net:1577</a></td>
    </tr>
    <tr>
      <td>Germany</td>
      <td>5</td>
      <td>vpn612823739.opengw.net:222</td>
      <td><a href="vpn612823739.opengw.net:222">vpn612823739.opengw.net:222</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>6</td>
      <td>vpn407782665.opengw.net</td>
      <td><a href="vpn407782665.opengw.net">vpn407782665.opengw.net</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>6</td>
      <td>vpn154142408.opengw.net:1333</td>
      <td><a href="vpn154142408.opengw.net:1333">vpn154142408.opengw.net:1333</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>8</td>
      <td>vpn350753023.opengw.net:1245</td>
      <td><a href="vpn350753023.opengw.net:1245">vpn350753023.opengw.net:1245</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>8</td>
      <td>vpn673829373.opengw.net:1920</td>
      <td><a href="vpn673829373.opengw.net:1920">vpn673829373.opengw.net:1920</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>8</td>
      <td>vpn319659443.opengw.net:1521</td>
      <td><a href="vpn319659443.opengw.net:1521">vpn319659443.opengw.net:1521</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>8</td>
      <td>vpn577648071.opengw.net:1795</td>
      <td><a href="vpn577648071.opengw.net:1795">vpn577648071.opengw.net:1795</a></td>
    </tr>
    <tr>
      <td>United States</td>
      <td>11</td>
      <td>vpn228965441.opengw.net:1358</td>
      <td><a href="vpn228965441.opengw.net:1358">vpn228965441.opengw.net:1358</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>12</td>
      <td>public-vpn-189.opengw.net</td>
      <td><a href="public-vpn-189.opengw.net">public-vpn-189.opengw.net</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>13</td>
      <td>vpn697491118.opengw.net:1590</td>
      <td><a href="vpn697491118.opengw.net:1590">vpn697491118.opengw.net:1590</a></td>
    </tr>
    <tr>
      <td>United States</td>
      <td>14</td>
      <td>vpn688802045.opengw.net:1995</td>
      <td><a href="vpn688802045.opengw.net:1995">vpn688802045.opengw.net:1995</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>14</td>
      <td>kozakura0623.opengw.net</td>
      <td><a href="kozakura0623.opengw.net">kozakura0623.opengw.net</a></td>
    </tr>
    <tr>
      <td>Russian Federation</td>
      <td>17</td>
      <td>vpn173522491.opengw.net:1759</td>
      <td><a href="vpn173522491.opengw.net:1759">vpn173522491.opengw.net:1759</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>19</td>
      <td>public-vpn-88.opengw.net</td>
      <td><a href="public-vpn-88.opengw.net">public-vpn-88.opengw.net</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>19</td>
      <td>vpn343424094.opengw.net:1333</td>
      <td><a href="vpn343424094.opengw.net:1333">vpn343424094.opengw.net:1333</a></td>
    </tr>
    <tr>
      <td>United States</td>
      <td>20</td>
      <td>vpn258117169.opengw.net:1920</td>
      <td><a href="vpn258117169.opengw.net:1920">vpn258117169.opengw.net:1920</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>26</td>
      <td>vpn338519318.opengw.net:1531</td>
      <td><a href="vpn338519318.opengw.net:1531">vpn338519318.opengw.net:1531</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>26</td>
      <td>vpn489593861.opengw.net:1620</td>
      <td><a href="vpn489593861.opengw.net:1620">vpn489593861.opengw.net:1620</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>27</td>
      <td>vpn778023538.opengw.net:1297</td>
      <td><a href="vpn778023538.opengw.net:1297">vpn778023538.opengw.net:1297</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>27</td>
      <td>vpn614520548.opengw.net:1205</td>
      <td><a href="vpn614520548.opengw.net:1205">vpn614520548.opengw.net:1205</a></td>
    </tr>
    <tr>
      <td>Thailand</td>
      <td>28</td>
      <td>vpn333522643.opengw.net:1413</td>
      <td><a href="vpn333522643.opengw.net:1413">vpn333522643.opengw.net:1413</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>29</td>
      <td>vpn403273662.opengw.net:995</td>
      <td><a href="vpn403273662.opengw.net:995">vpn403273662.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>29</td>
      <td>vpn499007311.opengw.net:995</td>
      <td><a href="vpn499007311.opengw.net:995">vpn499007311.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>29</td>
      <td>vpn244981678.opengw.net:1840</td>
      <td><a href="vpn244981678.opengw.net:1840">vpn244981678.opengw.net:1840</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>29</td>
      <td>public-vpn-250.opengw.net</td>
      <td><a href="public-vpn-250.opengw.net">public-vpn-250.opengw.net</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>29</td>
      <td>vpn368310195.opengw.net:1743</td>
      <td><a href="vpn368310195.opengw.net:1743">vpn368310195.opengw.net:1743</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>30</td>
      <td>vpn372705474.opengw.net:995</td>
      <td><a href="vpn372705474.opengw.net:995">vpn372705474.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>31</td>
      <td>vpn621971981.opengw.net:995</td>
      <td><a href="vpn621971981.opengw.net:995">vpn621971981.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>31</td>
      <td>vpn742294598.opengw.net:995</td>
      <td><a href="vpn742294598.opengw.net:995">vpn742294598.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>31</td>
      <td>vpn644001980.opengw.net:995</td>
      <td><a href="vpn644001980.opengw.net:995">vpn644001980.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>31</td>
      <td>vpn881525151.opengw.net:995</td>
      <td><a href="vpn881525151.opengw.net:995">vpn881525151.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>31</td>
      <td>vpn413096413.opengw.net:995</td>
      <td><a href="vpn413096413.opengw.net:995">vpn413096413.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>32</td>
      <td>public-vpn-137.opengw.net</td>
      <td><a href="public-vpn-137.opengw.net">public-vpn-137.opengw.net</a></td>
    </tr>
    <tr>
      <td>United States</td>
      <td>32</td>
      <td>vpn640405793.opengw.net:1922</td>
      <td><a href="vpn640405793.opengw.net:1922">vpn640405793.opengw.net:1922</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>32</td>
      <td>vpn854886126.opengw.net:995</td>
      <td><a href="vpn854886126.opengw.net:995">vpn854886126.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>32</td>
      <td>vpn774743846.opengw.net:995</td>
      <td><a href="vpn774743846.opengw.net:995">vpn774743846.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>32</td>
      <td>vpn595608604.opengw.net:1415</td>
      <td><a href="vpn595608604.opengw.net:1415">vpn595608604.opengw.net:1415</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>32</td>
      <td>vpn337618223.opengw.net:995</td>
      <td><a href="vpn337618223.opengw.net:995">vpn337618223.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>32</td>
      <td>vpn823495711.opengw.net:1461</td>
      <td><a href="vpn823495711.opengw.net:1461">vpn823495711.opengw.net:1461</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>32</td>
      <td>vpn101228790.opengw.net:1545</td>
      <td><a href="vpn101228790.opengw.net:1545">vpn101228790.opengw.net:1545</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>32</td>
      <td>vpn482460950.opengw.net:1962</td>
      <td><a href="vpn482460950.opengw.net:1962">vpn482460950.opengw.net:1962</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>32</td>
      <td>vpn721631364.opengw.net:1232</td>
      <td><a href="vpn721631364.opengw.net:1232">vpn721631364.opengw.net:1232</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>32</td>
      <td>vpn897003063.opengw.net:1546</td>
      <td><a href="vpn897003063.opengw.net:1546">vpn897003063.opengw.net:1546</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>33</td>
      <td>vpn929758859.opengw.net:1952</td>
      <td><a href="vpn929758859.opengw.net:1952">vpn929758859.opengw.net:1952</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>33</td>
      <td>vpn918645104.opengw.net:1729</td>
      <td><a href="vpn918645104.opengw.net:1729">vpn918645104.opengw.net:1729</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>33</td>
      <td>vpn324022834.opengw.net:1402</td>
      <td><a href="vpn324022834.opengw.net:1402">vpn324022834.opengw.net:1402</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>33</td>
      <td>vpn664594899.opengw.net:1694</td>
      <td><a href="vpn664594899.opengw.net:1694">vpn664594899.opengw.net:1694</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>34</td>
      <td>vpn864577769.opengw.net:995</td>
      <td><a href="vpn864577769.opengw.net:995">vpn864577769.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>37</td>
      <td>vpn846249695.opengw.net:995</td>
      <td><a href="vpn846249695.opengw.net:995">vpn846249695.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>37</td>
      <td>vpn490669373.opengw.net:1436</td>
      <td><a href="vpn490669373.opengw.net:1436">vpn490669373.opengw.net:1436</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>38</td>
      <td>vpn940577737.opengw.net:995</td>
      <td><a href="vpn940577737.opengw.net:995">vpn940577737.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>38</td>
      <td>vpn428379566.opengw.net:1860</td>
      <td><a href="vpn428379566.opengw.net:1860">vpn428379566.opengw.net:1860</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>38</td>
      <td>vpn477154162.opengw.net</td>
      <td><a href="vpn477154162.opengw.net">vpn477154162.opengw.net</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>38</td>
      <td>vpn887190747.opengw.net:1766</td>
      <td><a href="vpn887190747.opengw.net:1766">vpn887190747.opengw.net:1766</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>38</td>
      <td>vpn395083142.opengw.net:995</td>
      <td><a href="vpn395083142.opengw.net:995">vpn395083142.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>39</td>
      <td>vpn587464934.opengw.net:1909</td>
      <td><a href="vpn587464934.opengw.net:1909">vpn587464934.opengw.net:1909</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>39</td>
      <td>vpn515027798.opengw.net:1342</td>
      <td><a href="vpn515027798.opengw.net:1342">vpn515027798.opengw.net:1342</a></td>
    </tr>
    <tr>
      <td>Thailand</td>
      <td>39</td>
      <td>vpn243207756.opengw.net:1288</td>
      <td><a href="vpn243207756.opengw.net:1288">vpn243207756.opengw.net:1288</a></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>41</td>
      <td>vpn684044571.opengw.net:1344</td>
      <td><a href="vpn684044571.opengw.net:1344">vpn684044571.opengw.net:1344</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>41</td>
      <td>vpn653717896.opengw.net:1894</td>
      <td><a href="vpn653717896.opengw.net:1894">vpn653717896.opengw.net:1894</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>42</td>
      <td>vpn988633832.opengw.net:995</td>
      <td><a href="vpn988633832.opengw.net:995">vpn988633832.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Korea Republic of</td>
      <td>47</td>
      <td>vpn134247410.opengw.net:995</td>
      <td><a href="vpn134247410.opengw.net:995">vpn134247410.opengw.net:995</a></td>
    </tr>
    <tr>
      <td>Russian Federation</td>
      <td>48</td>
      <td>vpn397955876.opengw.net:1938</td>
      <td><a href="vpn397955876.opengw.net:1938">vpn397955876.opengw.net:1938</a></td>
    </tr>
    <tr>
      <td>Russian Federation</td>
      <td>57</td>
      <td>tlt.opengw.net:996</td>
      <td><a href="tlt.opengw.net:996">tlt.opengw.net:996</a></td>
    </tr>
  </tbody>
</table>
</body>
</html>
