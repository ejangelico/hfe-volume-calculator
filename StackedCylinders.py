import matplotlib.pyplot as plt
import numpy as np 

class StackedCylinders:
    def __init__(self, unit='inches'):
        self.cylinders = []
        self.unit = unit 


    def add_cylinder(self, radius, height, is_displacing=False, z=None):
        if(is_displacing and z is None):
            print("Need a z-value for displacing volumes")
            print("Not adding that cylinder")
            return
        
        if(is_displacing):
            self.cylinders.append((radius, height, is_displacing, z))
        else:
            #first is at z=0 
            if(z is None):
                if(len(self.cylinders) == 0):
                    self.cylinders.append((radius, height, is_displacing, 0))
                else:
                    self.cylinders.append((radius, height, is_displacing, self.cylinders[-1][1] + self.cylinders[-1][-1]))
                    print(self.cylinders[-1])
            else:
                self.cylinders.append((radius, height, is_displacing, z))


    def get_zrange(self):
        zs = [_[-1] for _ in self.cylinders]
        hs = [_[-1] + _[1] for _ in self.cylinders] #also add their heights over their zs
        zs = zs + hs
        return min(zs), max(zs)
    
    def get_radrange(self):
        rs = [_[0] for _ in self.cylinders]
        return min(rs), max(rs)

    def plot_configuration(self, show=True):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        for cylinder in self.cylinders:
            radius, height, is_displacing, z = cylinder

            if(is_displacing):
                rect = plt.Rectangle((-radius, z), 2*radius, height, color='k', alpha=0.5)
            else:
                rect = plt.Rectangle((-radius, z), 2*radius, height, alpha=0.5, linewidth=3)
            ax.add_patch(rect)

        xrange = self.get_radrange()
        zrange = self.get_zrange()
        ax.set_xlim(-xrange[1], xrange[1])
        ax.set_ylim(zrange[0], zrange[1])
        ax.set_xlabel("[in]")
        ax.set_ylabel("[in]")
        print(zrange)
        ax.grid(False)
        if(show): plt.show()
        return ax

    #find the volume from 0 to a particular height "zfill"
    def filled_volume(self, zfill):
        total_volume = 0

        for cylinder in self.cylinders:
            radius, cyl_height, is_displacing, z = cylinder

            #get the volume at this height, only nonzero if 
            #the zfill value is above the bottom level of the cylinder  
            if(zfill < z):
                volume = 0
            elif(z <= zfill <= z + cyl_height):
                volume = (zfill - z) * radius**2 * np.pi
            else:
                volume = (cyl_height) * radius**2 * np.pi

            if is_displacing:
                total_volume -= volume
            else:
                total_volume += volume

        #regardless, always report in L
        if(self.unit =='inches'):
            total_volume *= (2.545**3)/1000

        return total_volume #L
    
    #density in kg/L to get mass on other y axis. Default is lbs on other axis
    #because that's how we measure. Feel free to code in a switch for units. 
    def plot_volume_vs_height(self, ax=None, show=True, density=None):
        
        if(ax is None):
            fig, ax = plt.subplots()

        zrange = self.get_zrange()
        zs = np.linspace(min(zrange), max(zrange), 100)
        vols = np.array([self.filled_volume(_) for _ in zs])
        ax.plot(zs, vols)
        if(density != None):
            ax2 = ax.twinx()
            ax2.plot(zs, vols*density*2.2)
            ax2.set_ylabel("mass [lbs]")

        ax.set_xlabel("height of liquid [" + self.unit + "]")
        ax.set_ylabel("volume [L]")

        #plot thin lines corresponding to the z and height of displacing volumes
        for cylinder in self.cylinders:
            radius, cyl_height, is_displacing, z = cylinder
            if(is_displacing):
                ax.axvline(z + cyl_height, color='k', linewidth=0.5)
                ax.axvline(z, color='k', linewidth=0.5)



        if(show): plt.show()
        return ax

        

