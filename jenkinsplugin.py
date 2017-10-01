import shutit

s = shutit.create_session('bash',loglevel='info',echo=True)
s.login('docker run -ti ubuntu:16.04 bash')
s.install('maven')
s.send('mkdir -p /root/.m2')
s.send_file('/root/.m2/settings.xml','''<settings>
  <pluginGroups>
    <pluginGroup>org.jenkins-ci.tools</pluginGroup>
  </pluginGroups>

  <profiles>
    <!-- Give access to Jenkins plugins -->
    <profile>
      <id>jenkins</id>
      <activation>
        <activeByDefault>true</activeByDefault> 
          <!-- change this to false, if you don't like to have it on per default -->
      </activation>
      <repositories>
        <repository>
          <id>repo.jenkins-ci.org</id>
          <url>http://repo.jenkins-ci.org/public/</url>
        </repository>
      </repositories>
      <pluginRepositories>
        <pluginRepository>
          <id>repo.jenkins-ci.org</id>
          <url>http://repo.jenkins-ci.org/public/</url>
        </pluginRepository>
      </pluginRepositories>
    </profile>
  </profiles>
  <mirrors>
    <mirror>
      <id>repo.jenkins-ci.org</id>
      <url>http://repo.jenkins-ci.org/public/</url>
      <mirrorOf>m.g.o-public</mirrorOf>
    </mirror>
  </mirrors>
</settings>''')
s.send('mkdir -p /jenkinspluginexample')
s.send('cd /jenkinspluginexample')
s.multisend('mvn archetype:generate -Dfilter=io.jenkins.archetypes:',{'Choose archetype':'2',"""Define value for property 'artifactId'""":'imartifact1',"""Define value for property 'version'""":'','Y:':''})
s.send('cd imartifact1')
s.send('mvn package')
s.pause_point('')
s.logout()
